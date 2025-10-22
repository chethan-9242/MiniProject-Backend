"""
Flan-T5 Symptom Analysis Accuracy Evaluation
Comprehensive benchmarking and accuracy testing for the enhanced AI system
"""

import asyncio
import json
import time
from typing import List, Dict, Any, Tuple
from datetime import datetime
import statistics

# Import the new Flan-T5 service
from services.flan_t5_symptoms_service import get_flan_t5_symptoms_service

class FlanT5AccuracyEvaluator:
    """Comprehensive accuracy evaluator for Flan-T5 symptom analysis"""
    
    def __init__(self):
        self.service = get_flan_t5_symptoms_service()
        self.test_results = []
        
    def get_test_cases(self) -> List[Dict[str, Any]]:
        """Get comprehensive test cases with expected outcomes"""
        return [
            # Emergency Cases (Should detect as emergency)
            {
                "test_name": "Chest Pain Emergency",
                "symptoms": [
                    {"name": "severe chest pain", "severity": "severe", "duration": "30 minutes"},
                    {"name": "difficulty breathing", "severity": "severe", "duration": "1 hour"}
                ],
                "expected_emergency_level": "emergency",
                "expected_confidence_min": 0.85,
                "category": "emergency"
            },
            {
                "test_name": "Stroke Symptoms",
                "symptoms": [
                    {"name": "loss of consciousness", "severity": "severe", "duration": "10 minutes"},
                    {"name": "severe headache", "severity": "severe", "duration": "20 minutes"}
                ],
                "expected_emergency_level": "emergency",
                "expected_confidence_min": 0.85,
                "category": "emergency"
            },
            
            # Vata Dosha Cases
            {
                "test_name": "Classic Vata Imbalance",
                "symptoms": [
                    {"name": "anxiety", "severity": "moderate", "duration": "1 week"},
                    {"name": "insomnia", "severity": "moderate", "duration": "5 days"},
                    {"name": "constipation", "severity": "mild", "duration": "3 days"},
                    {"name": "dry skin", "severity": "mild", "duration": "2 weeks"}
                ],
                "expected_primary_dosha": "vata",
                "expected_conditions": ["anxiety disorders", "insomnia", "digestive issues"],
                "expected_confidence_min": 0.75,
                "category": "vata"
            },
            {
                "test_name": "Vata Nervous System",
                "symptoms": [
                    {"name": "nervousness", "severity": "moderate", "duration": "4 days"},
                    {"name": "restlessness", "severity": "moderate", "duration": "3 days"},
                    {"name": "joint pain", "severity": "mild", "duration": "1 week"}
                ],
                "expected_primary_dosha": "vata",
                "expected_confidence_min": 0.70,
                "category": "vata"
            },
            
            # Pitta Dosha Cases
            {
                "test_name": "Classic Pitta Imbalance",
                "symptoms": [
                    {"name": "heartburn", "severity": "moderate", "duration": "3 days"},
                    {"name": "acid reflux", "severity": "moderate", "duration": "1 week"},
                    {"name": "irritability", "severity": "mild", "duration": "5 days"},
                    {"name": "skin rash", "severity": "mild", "duration": "4 days"}
                ],
                "expected_primary_dosha": "pitta",
                "expected_conditions": ["acid reflux", "gastritis", "skin conditions"],
                "expected_confidence_min": 0.75,
                "category": "pitta"
            },
            {
                "test_name": "Pitta Heat Symptoms",
                "symptoms": [
                    {"name": "fever", "severity": "moderate", "duration": "2 days"},
                    {"name": "excessive sweating", "severity": "moderate", "duration": "3 days"},
                    {"name": "sensitivity to heat", "severity": "mild", "duration": "1 week"}
                ],
                "expected_primary_dosha": "pitta",
                "expected_confidence_min": 0.70,
                "category": "pitta"
            },
            
            # Kapha Dosha Cases
            {
                "test_name": "Classic Kapha Imbalance",
                "symptoms": [
                    {"name": "congestion", "severity": "moderate", "duration": "1 week"},
                    {"name": "cough with phlegm", "severity": "moderate", "duration": "5 days"},
                    {"name": "weight gain", "severity": "mild", "duration": "2 months"},
                    {"name": "sluggishness", "severity": "moderate", "duration": "2 weeks"}
                ],
                "expected_primary_dosha": "kapha",
                "expected_conditions": ["respiratory infection", "weight management", "lethargy"],
                "expected_confidence_min": 0.75,
                "category": "kapha"
            },
            {
                "test_name": "Kapha Depression",
                "symptoms": [
                    {"name": "depression", "severity": "moderate", "duration": "3 weeks"},
                    {"name": "excessive sleep", "severity": "moderate", "duration": "2 weeks"},
                    {"name": "lethargy", "severity": "moderate", "duration": "1 month"}
                ],
                "expected_primary_dosha": "kapha",
                "expected_confidence_min": 0.70,
                "category": "kapha"
            },
            
            # Common Conditions
            {
                "test_name": "Common Cold",
                "symptoms": [
                    {"name": "runny nose", "severity": "mild", "duration": "3 days"},
                    {"name": "sore throat", "severity": "mild", "duration": "2 days"},
                    {"name": "cough", "severity": "mild", "duration": "4 days"},
                    {"name": "fatigue", "severity": "mild", "duration": "3 days"}
                ],
                "expected_conditions": ["common cold", "viral infection", "respiratory infection"],
                "expected_confidence_min": 0.70,
                "category": "common"
            },
            {
                "test_name": "Digestive Issues",
                "symptoms": [
                    {"name": "stomach pain", "severity": "moderate", "duration": "2 days"},
                    {"name": "nausea", "severity": "mild", "duration": "1 day"},
                    {"name": "bloating", "severity": "moderate", "duration": "3 days"}
                ],
                "expected_conditions": ["indigestion", "gastritis", "digestive disorder"],
                "expected_confidence_min": 0.70,
                "category": "common"
            },
            
            # Urgent Cases (Non-emergency but needs attention)
            {
                "test_name": "Persistent High Fever",
                "symptoms": [
                    {"name": "high fever", "severity": "severe", "duration": "4 days"},
                    {"name": "severe fatigue", "severity": "severe", "duration": "5 days"}
                ],
                "expected_emergency_level": "urgent",
                "expected_confidence_min": 0.75,
                "category": "urgent"
            }
        ]
    
    async def evaluate_single_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a single test case"""
        print(f"Testing: {test_case['test_name']}...")
        
        start_time = time.time()
        try:
            # Run the analysis
            result = await self.service.analyze_symptoms_with_flan_t5(
                symptoms=test_case["symptoms"],
                patient_context={"age": 35, "gender": "unspecified"}
            )
            
            processing_time = time.time() - start_time
            
            # Evaluate results
            evaluation = self._evaluate_result(test_case, result)
            evaluation["processing_time"] = processing_time
            evaluation["success"] = True
            
            return evaluation
            
        except Exception as e:
            processing_time = time.time() - start_time
            return {
                "test_name": test_case["test_name"],
                "success": False,
                "error": str(e),
                "processing_time": processing_time,
                "category": test_case["category"],
                "score": 0.0
            }
    
    def _evaluate_result(self, test_case: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the analysis result against expected outcomes"""
        evaluation = {
            "test_name": test_case["test_name"],
            "category": test_case["category"],
            "scores": {},
            "details": {},
            "overall_score": 0.0
        }
        
        total_score = 0.0
        max_score = 0.0
        
        # Check emergency level (if expected)
        if "expected_emergency_level" in test_case:
            max_score += 30  # 30% weight for emergency detection
            actual_level = result.get("medical_guidance", {}).get("urgency_level", "routine")
            expected_level = test_case["expected_emergency_level"]
            
            if actual_level == expected_level:
                total_score += 30
                evaluation["scores"]["emergency_detection"] = 100
                evaluation["details"]["emergency"] = f"✅ Correctly detected {expected_level}"
            else:
                evaluation["scores"]["emergency_detection"] = 0
                evaluation["details"]["emergency"] = f"❌ Expected {expected_level}, got {actual_level}"
        
        # Check dosha analysis (if expected)
        if "expected_primary_dosha" in test_case:
            max_score += 25  # 25% weight for dosha accuracy
            dosha_analysis = result.get("dosha_analysis", {})
            actual_dosha = dosha_analysis.get("primary_imbalance", "").lower()
            expected_dosha = test_case["expected_primary_dosha"].lower()
            
            if expected_dosha in actual_dosha:
                total_score += 25
                evaluation["scores"]["dosha_accuracy"] = 100
                evaluation["details"]["dosha"] = f"✅ Correctly identified {expected_dosha.title()} dosha"
            else:
                evaluation["scores"]["dosha_accuracy"] = 0
                evaluation["details"]["dosha"] = f"❌ Expected {expected_dosha.title()}, got {actual_dosha.title()}"
        
        # Check condition identification (if expected)
        if "expected_conditions" in test_case:
            max_score += 25  # 25% weight for condition accuracy
            conditions = result.get("possible_conditions", [])
            condition_names = [c.get("name", "").lower() for c in conditions]
            expected_conditions = [c.lower() for c in test_case["expected_conditions"]]
            
            matches = 0
            for expected in expected_conditions:
                for actual in condition_names:
                    if any(word in actual for word in expected.split()):
                        matches += 1
                        break
            
            condition_score = (matches / len(expected_conditions)) * 25 if expected_conditions else 0
            total_score += condition_score
            evaluation["scores"]["condition_accuracy"] = (matches / len(expected_conditions)) * 100 if expected_conditions else 0
            evaluation["details"]["conditions"] = f"Matched {matches}/{len(expected_conditions)} expected conditions"
        
        # Check confidence level
        max_score += 20  # 20% weight for confidence
        confidence = result.get("confidence_metrics", {}).get("overall_confidence", 0.0)
        min_confidence = test_case.get("expected_confidence_min", 0.7)
        
        if confidence >= min_confidence:
            total_score += 20
            evaluation["scores"]["confidence_level"] = 100
            evaluation["details"]["confidence"] = f"✅ Confidence {confidence:.2%} >= {min_confidence:.2%}"
        else:
            confidence_score = (confidence / min_confidence) * 20
            total_score += confidence_score
            evaluation["scores"]["confidence_level"] = (confidence / min_confidence) * 100
            evaluation["details"]["confidence"] = f"⚠️ Confidence {confidence:.2%} < {min_confidence:.2%}"
        
        # Overall score
        evaluation["overall_score"] = (total_score / max_score * 100) if max_score > 0 else 0
        
        return evaluation
    
    async def run_comprehensive_evaluation(self) -> Dict[str, Any]:
        """Run comprehensive accuracy evaluation"""
        print("🚀 Starting Comprehensive Flan-T5 Accuracy Evaluation\n")
        print("="*60)
        
        test_cases = self.get_test_cases()
        results = []
        
        start_time = time.time()
        
        # Run all test cases
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n[{i}/{len(test_cases)}] {test_case['test_name']}")
            result = await self.evaluate_single_case(test_case)
            results.append(result)
            
            # Show immediate result
            if result["success"]:
                print(f"   Score: {result['overall_score']:.1f}% | Time: {result['processing_time']:.2f}s")
                for detail in result.get("details", {}).values():
                    print(f"   {detail}")
            else:
                print(f"   ❌ Failed: {result['error']}")
        
        total_time = time.time() - start_time
        
        # Calculate overall statistics
        successful_results = [r for r in results if r["success"]]
        
        if successful_results:
            scores = [r["overall_score"] for r in successful_results]
            processing_times = [r["processing_time"] for r in successful_results]
            
            overall_stats = {
                "total_tests": len(test_cases),
                "successful_tests": len(successful_results),
                "success_rate": len(successful_results) / len(test_cases) * 100,
                "average_accuracy": statistics.mean(scores),
                "median_accuracy": statistics.median(scores),
                "min_accuracy": min(scores),
                "max_accuracy": max(scores),
                "accuracy_std": statistics.stdev(scores) if len(scores) > 1 else 0,
                "average_processing_time": statistics.mean(processing_times),
                "total_evaluation_time": total_time
            }
            
            # Category-wise breakdown
            categories = {}
            for result in successful_results:
                cat = result["category"]
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(result["overall_score"])
            
            category_stats = {}
            for cat, scores in categories.items():
                category_stats[cat] = {
                    "count": len(scores),
                    "average_accuracy": statistics.mean(scores),
                    "min_accuracy": min(scores),
                    "max_accuracy": max(scores)
                }
            
            # Generate final report
            self._print_final_report(overall_stats, category_stats, results)
            
            return {
                "overall_statistics": overall_stats,
                "category_statistics": category_stats,
                "detailed_results": results,
                "evaluation_timestamp": datetime.now().isoformat(),
                "model_info": {
                    "model_type": "Google Flan-T5 Large",
                    "analysis_method": "LLM + RAG + Knowledge Base",
                    "version": "2.0"
                }
            }
        
        else:
            print("\n❌ All tests failed. System appears to have critical issues.")
            return {
                "overall_statistics": {"success_rate": 0, "average_accuracy": 0},
                "detailed_results": results
            }
    
    def _print_final_report(self, overall_stats: Dict, category_stats: Dict, results: List[Dict]):
        """Print comprehensive final report"""
        print("\n" + "="*60)
        print("📊 FLAN-T5 SYMPTOM ANALYSIS ACCURACY REPORT")
        print("="*60)
        
        # Overall Performance
        print(f"\n🎯 OVERALL PERFORMANCE:")
        print(f"   Success Rate: {overall_stats['success_rate']:.1f}% ({overall_stats['successful_tests']}/{overall_stats['total_tests']} tests)")
        print(f"   Average Accuracy: {overall_stats['average_accuracy']:.1f}%")
        print(f"   Median Accuracy: {overall_stats['median_accuracy']:.1f}%")
        print(f"   Range: {overall_stats['min_accuracy']:.1f}% - {overall_stats['max_accuracy']:.1f}%")
        print(f"   Standard Deviation: ±{overall_stats['accuracy_std']:.1f}%")
        
        # Performance Comparison with Old System
        print(f"\n📈 IMPROVEMENT OVER OLD SYSTEM:")
        old_accuracy = 15.7  # From symptom_model_info.json
        improvement = overall_stats['average_accuracy'] - old_accuracy
        improvement_factor = overall_stats['average_accuracy'] / old_accuracy if old_accuracy > 0 else 0
        
        print(f"   Old ML Model (Logistic Regression): {old_accuracy:.1f}%")
        print(f"   New Flan-T5 System: {overall_stats['average_accuracy']:.1f}%")
        print(f"   Improvement: +{improvement:.1f} percentage points")
        print(f"   Performance Factor: {improvement_factor:.1f}x better")
        
        # Category Breakdown
        print(f"\n📋 CATEGORY BREAKDOWN:")
        for category, stats in category_stats.items():
            print(f"   {category.upper():12}: {stats['average_accuracy']:5.1f}% avg | Range: {stats['min_accuracy']:.1f}%-{stats['max_accuracy']:.1f}% | ({stats['count']} tests)")
        
        # Performance Metrics
        print(f"\n⚡ PERFORMANCE METRICS:")
        print(f"   Average Processing Time: {overall_stats['average_processing_time']:.2f}s per analysis")
        print(f"   Total Evaluation Time: {overall_stats['total_evaluation_time']:.1f}s")
        
        # Grade Assignment
        avg_accuracy = overall_stats['average_accuracy']
        if avg_accuracy >= 90:
            grade = "A+ (Excellent)"
            status = "🏆 EXCEPTIONAL PERFORMANCE"
        elif avg_accuracy >= 80:
            grade = "A (Very Good)"
            status = "✅ HIGH PERFORMANCE"
        elif avg_accuracy >= 70:
            grade = "B (Good)"
            status = "👍 GOOD PERFORMANCE"
        elif avg_accuracy >= 60:
            grade = "C (Fair)"
            status = "⚠️ ACCEPTABLE PERFORMANCE"
        else:
            grade = "D (Needs Improvement)"
            status = "❌ REQUIRES ATTENTION"
        
        print(f"\n🏆 SYSTEM GRADE: {grade}")
        print(f"   Status: {status}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if avg_accuracy >= 80:
            print("   • System performing excellently - ready for production")
            print("   • Consider fine-tuning for specific edge cases")
        elif avg_accuracy >= 70:
            print("   • System performing well - suitable for most use cases")
            print("   • Monitor edge cases and continue optimization")
        elif avg_accuracy >= 60:
            print("   • System functional but needs improvement")
            print("   • Focus on enhancing knowledge base and prompts")
        else:
            print("   • System needs significant improvement before deployment")
            print("   • Review model configuration and knowledge base")
        
        print("   • Continue monitoring real-world performance")
        print("   • Gather user feedback for continuous improvement")

async def main():
    """Main evaluation function"""
    evaluator = FlanT5AccuracyEvaluator()
    
    try:
        results = await evaluator.run_comprehensive_evaluation()
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"flan_t5_accuracy_report_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Detailed report saved to: {report_file}")
        
    except Exception as e:
        print(f"\n💥 Evaluation failed: {str(e)}")
        print("This might indicate configuration or dependency issues.")

if __name__ == "__main__":
    asyncio.run(main())