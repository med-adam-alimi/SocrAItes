#!/usr/bin/env python3
"""
Comprehensive SocrAItes Testing Suite
Tests all philosophers, endpoints, and performance
"""

import requests
import time
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

class SocrAItesTestSuite:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.philosophers = ['camus', 'nietzsche', 'dostoevsky', 'socrates', 'kafka', 'cioran']
        self.test_questions = [
            "What is the meaning of life?",
            "How should we deal with suffering?", 
            "What is freedom?",
            "Is there hope in despair?",
            "How do we find purpose?"
        ]
        self.results = {
            'passed': 0,
            'failed': 0,
            'total_time': 0,
            'errors': []
        }
    
    def test_server_health(self):
        """Test if server is running"""
        print("🏥 Testing server health...")
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                print("✅ Server is healthy")
                return True
            else:
                print(f"❌ Server returned {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Server health check failed: {e}")
            return False
    
    def test_philosophers_endpoint(self):
        """Test philosophers list endpoint"""
        print("👨‍🏫 Testing philosophers endpoint...")
        try:
            response = requests.get(f"{self.base_url}/api/philosophers", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'philosophers' in data and len(data['philosophers']) >= 6:
                    print(f"✅ Philosophers endpoint working - {len(data['philosophers'])} philosophers")
                    return True
                else:
                    print("❌ Philosophers endpoint returned invalid data")
                    return False
        except Exception as e:
            print(f"❌ Philosophers endpoint failed: {e}")
            return False
    
    def test_chat_endpoint(self, philosopher, question):
        """Test individual chat endpoint"""
        start_time = time.time()
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={'message': question, 'philosopher': philosopher},
                timeout=30
            )
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                if 'response' in data and len(data['response']) > 50:
                    status = "✅" if response_time < 5 else "⚡" if response_time < 10 else "🐌"
                    print(f"{status} {philosopher.title()}: {response_time:.2f}s - {data['response'][:80]}...")
                    return True, response_time
                else:
                    print(f"❌ {philosopher}: Invalid response format")
                    return False, response_time
            else:
                print(f"❌ {philosopher}: HTTP {response.status_code}")
                return False, response_time
                
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            print(f"❌ {philosopher}: Exception - {e}")
            return False, response_time
    
    def test_streaming_endpoint(self, philosopher, question):
        """Test streaming chat endpoint"""
        print(f"🌊 Testing streaming for {philosopher}...")
        try:
            response = requests.post(
                f"{self.base_url}/api/chat/stream",
                json={'message': question, 'philosopher': philosopher},
                timeout=30,
                stream=True
            )
            
            if response.status_code == 200:
                chunks_received = 0
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            try:
                                data = json.loads(line[6:])
                                chunks_received += 1
                                if data.get('type') == 'complete':
                                    print(f"✅ Streaming works: {chunks_received} chunks received")
                                    return True
                            except json.JSONDecodeError:
                                continue
                
                if chunks_received > 0:
                    print(f"⚡ Streaming partial: {chunks_received} chunks")
                    return True
                else:
                    print("❌ Streaming: No valid chunks received")
                    return False
            else:
                print(f"❌ Streaming: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Streaming failed: {e}")
            return False
    
    def test_all_philosophers(self):
        """Test all philosophers with sample questions"""
        print("\n🧠 Testing all philosophers...")
        print("=" * 60)
        
        philosopher_results = {}
        
        for philosopher in self.philosophers:
            print(f"\n🎭 Testing {philosopher.title()}...")
            
            # Test regular chat
            success, response_time = self.test_chat_endpoint(
                philosopher, 
                "What is your core philosophy?"
            )
            
            philosopher_results[philosopher] = {
                'chat_success': success,
                'response_time': response_time,
                'streaming_success': False
            }
            
            if success:
                self.results['passed'] += 1
                self.results['total_time'] += response_time
                
                # Test streaming if chat works
                streaming_success = self.test_streaming_endpoint(
                    philosopher,
                    "Tell me something brief."
                )
                philosopher_results[philosopher]['streaming_success'] = streaming_success
                
            else:
                self.results['failed'] += 1
                self.results['errors'].append(f"{philosopher} chat failed")
        
        return philosopher_results
    
    def test_performance_benchmark(self):
        """Performance benchmark with concurrent requests"""
        print("\n⚡ Performance Benchmark...")
        print("=" * 40)
        
        test_cases = [
            ('camus', 'What is absurdity?'),
            ('nietzsche', 'What is power?'),
            ('dostoevsky', 'What is suffering?')
        ]
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for philosopher, question in test_cases:
                future = executor.submit(self.test_chat_endpoint, philosopher, question)
                futures.append((philosopher, future))
            
            concurrent_results = []
            for philosopher, future in futures:
                try:
                    success, response_time = future.result(timeout=30)
                    concurrent_results.append((philosopher, success, response_time))
                except Exception as e:
                    concurrent_results.append((philosopher, False, 30.0))
        
        total_time = time.time() - start_time
        
        print(f"\n📊 Concurrent test completed in {total_time:.2f}s")
        for philosopher, success, resp_time in concurrent_results:
            status = "✅" if success else "❌"
            print(f"{status} {philosopher}: {resp_time:.2f}s")
        
        return concurrent_results
    
    def run_full_suite(self):
        """Run complete test suite"""
        print("🧪 SocrAItes Comprehensive Test Suite")
        print("=" * 50)
        
        # Test 1: Server Health
        if not self.test_server_health():
            print("❌ CRITICAL: Server is not responding!")
            return False
        
        # Test 2: API Endpoints
        if not self.test_philosophers_endpoint():
            print("❌ CRITICAL: Philosophers endpoint failed!")
            return False
        
        # Test 3: All Philosophers
        philosopher_results = self.test_all_philosophers()
        
        # Test 4: Performance Benchmark
        concurrent_results = self.test_performance_benchmark()
        
        # Generate Report
        self.generate_report(philosopher_results, concurrent_results)
        
        return self.results['failed'] == 0
    
    def generate_report(self, philosopher_results, concurrent_results):
        """Generate comprehensive test report"""
        print("\n📋 TEST REPORT")
        print("=" * 50)
        
        # Overall Stats
        total_tests = self.results['passed'] + self.results['failed']
        success_rate = (self.results['passed'] / total_tests * 100) if total_tests > 0 else 0
        avg_response_time = (self.results['total_time'] / self.results['passed']) if self.results['passed'] > 0 else 0
        
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        print(f"⏱️ Average Response Time: {avg_response_time:.2f}s")
        
        # Performance Assessment
        if avg_response_time < 3:
            print("🚀 EXCELLENT: Response times under 3 seconds!")
        elif avg_response_time < 5:
            print("⚡ GOOD: Response times under 5 seconds")
        elif avg_response_time < 10:
            print("⚠️ ACCEPTABLE: Response times under 10 seconds")
        else:
            print("🐌 SLOW: Response times over 10 seconds - needs optimization")
        
        # Philosopher Status
        print("\n🎭 Philosopher Status:")
        for philosopher, results in philosopher_results.items():
            chat_status = "✅" if results['chat_success'] else "❌"
            stream_status = "🌊" if results['streaming_success'] else "⭕"
            time_str = f"{results['response_time']:.2f}s"
            print(f"{chat_status}{stream_status} {philosopher.title()}: {time_str}")
        
        # Errors
        if self.results['errors']:
            print("\n❌ Errors Encountered:")
            for error in self.results['errors']:
                print(f"  • {error}")
        
        # Final Verdict
        print("\n🎯 FINAL VERDICT:")
        if self.results['failed'] == 0 and avg_response_time < 5:
            print("🎉 READY FOR PRODUCTION! All tests passed with good performance.")
        elif self.results['failed'] == 0:
            print("✅ FUNCTIONAL but could be faster. Ready for GitHub with notes.")
        else:
            print("⚠️ ISSUES DETECTED. Fix errors before deployment.")

def main():
    """Main test execution"""
    tester = SocrAItesTestSuite()
    
    print("🚀 Starting SocrAItes Test Suite...")
    print("⏰ This will take 2-3 minutes to complete thoroughly...")
    print()
    
    success = tester.run_full_suite()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! Ready for GitHub! 🚀")
        sys.exit(0)
    else:
        print("\n⚠️ Some tests failed. Review and fix issues before deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main()