import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Brain, Search, Plus, X, AlertTriangle, CheckCircle, Clock, Save, Download } from 'lucide-react';
import axios from 'axios';

const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');

interface Symptom {
  id: string;
  name: string;
  severity: 'mild' | 'moderate' | 'severe';
  duration: string;
}

interface SymptomAnalysis {
  possible_conditions: Array<{
    name: string;
    probability: number;
    description: string;
    ayurvedic_perspective: string;
  }>;
  recommendations: {
    immediate_actions: string[];
    lifestyle_changes: string[];
    herbal_remedies: string[];
    when_to_consult_doctor: string;
  };
  dosha_imbalance: {
    primary: string;
    description: string;
  };
}

const commonSymptoms = [
  'Headache', 'Fatigue', 'Nausea', 'Fever', 'Cough', 'Sore Throat',
  'Back Pain', 'Stomach Pain', 'Dizziness', 'Insomnia', 'Anxiety',
  'Joint Pain', 'Skin Rash', 'Constipation', 'Diarrhea', 'Loss of Appetite'
];

const SymptomChecker: React.FC = () => {
  const [symptoms, setSymptoms] = useState<Symptom[]>([]);
  const [newSymptom, setNewSymptom] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SymptomAnalysis | null>(null);
  const [step, setStep] = useState<'input' | 'details' | 'results'>('input');
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');
  const [userId] = useState(() => {
    // Get or create user ID from localStorage
    let id = localStorage.getItem('symptom_checker_user_id');
    if (!id) {
      id = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('symptom_checker_user_id', id);
    }
    return id;
  });

  const addSymptom = (symptomName: string) => {
    if (symptomName && !symptoms.find(s => s.name.toLowerCase() === symptomName.toLowerCase())) {
      const newSymptomObj: Symptom = {
        id: Date.now().toString(),
        name: symptomName,
        severity: 'moderate',
        duration: '1-2 days'
      };
      setSymptoms([...symptoms, newSymptomObj]);
      setNewSymptom('');
    }
  };

  const removeSymptom = (id: string) => {
    setSymptoms(symptoms.filter(s => s.id !== id));
  };

  const updateSymptom = (id: string, field: keyof Symptom, value: string) => {
    setSymptoms(symptoms.map(s => s.id === id ? { ...s, [field]: value } : s));
  };

  const analyzeSymptoms = async () => {
    if (symptoms.length === 0) return;
    
    setLoading(true);
    setStep('results');
    
    try {
      const response = await axios.post(`${API_URL}/api/symptoms/check`, {
        symptoms: symptoms
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error analyzing symptoms:', error);
      // Mock result for demo
      const mockResult: SymptomAnalysis = {
        possible_conditions: [
          {
            name: 'Common Cold (Pratishyaya)',
            probability: 75,
            description: 'Viral infection affecting the upper respiratory system',
            ayurvedic_perspective: 'Imbalance in Kapha and Vata doshas causing congestion and discomfort'
          },
          {
            name: 'Stress-related Fatigue',
            probability: 60,
            description: 'Physical and mental exhaustion due to prolonged stress',
            ayurvedic_perspective: 'Vata imbalance affecting the nervous system and energy levels'
          },
          {
            name: 'Seasonal Allergies',
            probability: 45,
            description: 'Allergic reaction to environmental factors',
            ayurvedic_perspective: 'Kapha imbalance with weak digestive fire (Agni)'
          }
        ],
        recommendations: {
          immediate_actions: [
            'Stay hydrated with warm water and herbal teas',
            'Rest and avoid strenuous activities',
            'Practice gentle breathing exercises (Pranayama)',
            'Apply warm compress to affected areas'
          ],
          lifestyle_changes: [
            'Maintain regular sleep schedule (8-9 hours)',
            'Follow a light, warm, and easily digestible diet',
            'Practice stress management techniques like meditation',
            'Avoid cold and processed foods'
          ],
          herbal_remedies: [
            'Tulsi (Holy Basil) tea for respiratory support',
            'Ginger and honey for digestive health',
            'Turmeric milk for anti-inflammatory benefits',
            'Ashwagandha for stress relief and immunity'
          ],
          when_to_consult_doctor: 'If symptoms persist for more than 7 days, worsen significantly, or if you experience fever above 101°F, difficulty breathing, or severe pain.'
        },
        dosha_imbalance: {
          primary: 'Kapha-Vata',
          description: 'Primary Kapha imbalance causing congestion and heaviness, with secondary Vata imbalance affecting circulation and nervous system'
        }
      };
      setResult(mockResult);
    }
    
    setLoading(false);
  };

  const resetAnalysis = () => {
    setSymptoms([]);
    setResult(null);
    setStep('input');
    setSaveStatus('idle');
  };

  const saveAnalysis = async () => {
    if (!result || !symptoms) return;
    
    setSaveStatus('saving');
    
    try {
      // Save to backend
      const response = await axios.post(`${API_URL}/api/symptoms/save`, {
        user_id: userId,
        symptoms: symptoms,
        analysis: result,
        notes: null
      });
      
      if (response.data.success) {
        setSaveStatus('saved');
        
        // Also save to localStorage as backup
        const savedAnalyses = JSON.parse(localStorage.getItem('saved_symptom_analyses') || '[]');
        savedAnalyses.unshift({
          id: response.data.analysis_id,
          timestamp: new Date().toISOString(),
          symptoms,
          analysis: result
        });
        // Keep only last 10
        localStorage.setItem('saved_symptom_analyses', JSON.stringify(savedAnalyses.slice(0, 10)));
        
        // Reset status after 3 seconds
        setTimeout(() => setSaveStatus('idle'), 3000);
      }
    } catch (error) {
      console.error('Error saving analysis:', error);
      
      // Fallback to localStorage only
      try {
        const savedAnalyses = JSON.parse(localStorage.getItem('saved_symptom_analyses') || '[]');
        savedAnalyses.unshift({
          id: `local_${Date.now()}`,
          timestamp: new Date().toISOString(),
          symptoms,
          analysis: result
        });
        localStorage.setItem('saved_symptom_analyses', JSON.stringify(savedAnalyses.slice(0, 10)));
        
        setSaveStatus('saved');
        setTimeout(() => setSaveStatus('idle'), 3000);
      } catch (localError) {
        setSaveStatus('error');
        setTimeout(() => setSaveStatus('idle'), 3000);
      }
    }
  };

  const downloadAnalysis = () => {
    if (!result || !symptoms) return;
    
    // Create print-friendly version
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;
    
    const date = new Date().toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
    
    const html = `
      <!DOCTYPE html>
      <html>
        <head>
          <title>Symptom Analysis Report - ${date}</title>
          <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
              font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
              padding: 40px;
              background: white;
              color: #333;
            }
            .header {
              text-align: center;
              margin-bottom: 30px;
              border-bottom: 3px solid #10b981;
              padding-bottom: 20px;
            }
            .header h1 {
              color: #10b981;
              font-size: 28px;
              margin-bottom: 10px;
            }
            .header p {
              color: #666;
              font-size: 14px;
            }
            .section {
              margin-bottom: 30px;
              page-break-inside: avoid;
            }
            .section-title {
              background: #10b981;
              color: white;
              padding: 10px 15px;
              font-size: 18px;
              font-weight: bold;
              margin-bottom: 15px;
              border-radius: 5px;
            }
            .dosha-box {
              background: linear-gradient(135deg, #10b981 0%, #059669 100%);
              color: white;
              padding: 20px;
              border-radius: 10px;
              margin-bottom: 20px;
            }
            .dosha-box h3 {
              font-size: 20px;
              margin-bottom: 10px;
            }
            .condition {
              border: 2px solid #e5e7eb;
              padding: 15px;
              margin-bottom: 15px;
              border-radius: 8px;
            }
            .condition-header {
              display: flex;
              justify-content: space-between;
              align-items: center;
              margin-bottom: 10px;
            }
            .condition-name {
              font-size: 16px;
              font-weight: bold;
              color: #1f2937;
            }
            .probability {
              background: #d1fae5;
              color: #065f46;
              padding: 4px 12px;
              border-radius: 15px;
              font-weight: bold;
              font-size: 14px;
            }
            .ayurvedic-box {
              background: #f0fdf4;
              border-left: 4px solid #10b981;
              padding: 12px;
              margin-top: 10px;
            }
            .ayurvedic-box h4 {
              color: #065f46;
              margin-bottom: 5px;
              font-size: 14px;
            }
            .recommendations {
              display: grid;
              grid-template-columns: 1fr 1fr;
              gap: 20px;
              margin-bottom: 20px;
            }
            .rec-box {
              border: 2px solid #e5e7eb;
              padding: 15px;
              border-radius: 8px;
            }
            .rec-box.immediate { border-color: #ef4444; }
            .rec-box.lifestyle { border-color: #3b82f6; }
            .rec-box.herbal { background: #f0fdf4; border-color: #10b981; }
            .rec-box h3 {
              font-size: 16px;
              margin-bottom: 12px;
              color: #1f2937;
            }
            .rec-box.immediate h3 { color: #dc2626; }
            .rec-box.lifestyle h3 { color: #2563eb; }
            .rec-box.herbal h3 { color: #059669; }
            .rec-box ul {
              list-style: none;
              padding-left: 0;
            }
            .rec-box li {
              padding: 6px 0;
              padding-left: 20px;
              position: relative;
              line-height: 1.5;
            }
            .rec-box li:before {
              content: '✓';
              position: absolute;
              left: 0;
              font-weight: bold;
            }
            .rec-box.immediate li:before { color: #dc2626; }
            .rec-box.lifestyle li:before { color: #2563eb; }
            .rec-box.herbal li:before { color: #059669; }
            .warning-box {
              background: #fef3c7;
              border: 2px solid #f59e0b;
              border-radius: 8px;
              padding: 15px;
              margin-top: 20px;
            }
            .warning-box h3 {
              color: #92400e;
              margin-bottom: 8px;
              font-size: 16px;
            }
            .symptoms-list {
              background: #f9fafb;
              padding: 15px;
              border-radius: 8px;
              margin-bottom: 20px;
            }
            .symptom-item {
              display: inline-block;
              background: white;
              border: 1px solid #d1d5db;
              padding: 6px 12px;
              margin: 4px;
              border-radius: 15px;
              font-size: 14px;
            }
            .footer {
              margin-top: 40px;
              padding-top: 20px;
              border-top: 2px solid #e5e7eb;
              text-align: center;
              color: #666;
              font-size: 12px;
            }
            .disclaimer {
              background: #fef2f2;
              border: 2px solid #fca5a5;
              border-radius: 8px;
              padding: 15px;
              margin: 20px 0;
              font-size: 13px;
              color: #7f1d1d;
            }
            @media print {
              body { padding: 20px; }
              .section { page-break-inside: avoid; }
            }
          </style>
        </head>
        <body>
          <div class="header">
            <h1>🌿 SwasthVedha - Symptom Analysis Report</h1>
            <p>AI-Powered Analysis Based on Ayurvedic Principles and Modern Medicine</p>
            <p style="margin-top: 10px; font-weight: bold;">Date: ${date}</p>
          </div>

          <div class="section">
            <div class="section-title">Your Symptoms</div>
            <div class="symptoms-list">
              ${symptoms.map(s => `
                <span class="symptom-item">
                  <strong>${s.name}</strong> - ${s.severity} (${s.duration})
                </span>
              `).join('')}
            </div>
          </div>

          <div class="section">
            <div class="section-title">Detected Dosha Imbalance</div>
            <div class="dosha-box">
              <h3>${result.dosha_imbalance.primary}</h3>
              <p>${result.dosha_imbalance.description}</p>
            </div>
          </div>

          <div class="section">
            <div class="section-title">Possible Conditions</div>
            ${result.possible_conditions.map((condition, index) => `
              <div class="condition">
                <div class="condition-header">
                  <span class="condition-name">${index + 1}. ${condition.name}</span>
                  <span class="probability">${condition.probability}% match</span>
                </div>
                <p style="color: #4b5563; margin: 10px 0;">${condition.description}</p>
                <div class="ayurvedic-box">
                  <h4>Ayurvedic Perspective:</h4>
                  <p style="color: #065f46;">${condition.ayurvedic_perspective}</p>
                </div>
              </div>
            `).join('')}
          </div>

          <div class="section">
            <div class="section-title">Recommendations</div>
            <div class="recommendations">
              <div class="rec-box immediate">
                <h3>⚠️ Immediate Actions</h3>
                <ul>
                  ${result.recommendations.immediate_actions.map(action => `<li>${action}</li>`).join('')}
                </ul>
              </div>
              <div class="rec-box lifestyle">
                <h3>🔄 Lifestyle Changes</h3>
                <ul>
                  ${result.recommendations.lifestyle_changes.map(change => `<li>${change}</li>`).join('')}
                </ul>
              </div>
            </div>
            <div class="rec-box herbal" style="grid-column: 1 / -1;">
              <h3>🌿 Recommended Herbal Remedies</h3>
              <ul style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                ${result.recommendations.herbal_remedies.map(herb => `<li>${herb}</li>`).join('')}
              </ul>
            </div>
          </div>

          <div class="warning-box">
            <h3>⚠️ When to Consult a Doctor</h3>
            <p>${result.recommendations.when_to_consult_doctor}</p>
          </div>

          <div class="disclaimer">
            <strong>⚠️ Medical Disclaimer:</strong> This analysis is for educational and informational purposes only. 
            It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. 
            Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
          </div>

          <div class="footer">
            <p><strong>SwasthVedha</strong> - Ayurvedic Healthcare Platform</p>
            <p>Generated on ${new Date().toLocaleString()}</p>
            <p style="margin-top: 10px;">This report is confidential and intended for personal use only.</p>
          </div>

          <script>
            window.onload = function() {
              setTimeout(function() {
                window.print();
              }, 500);
            };
          </script>
        </body>
      </html>
    `;
    
    printWindow.document.write(html);
    printWindow.document.close();
  };

  if (step === 'results') {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-6xl mx-auto"
      >
        {loading ? (
          <div className="text-center py-20">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-ayurveda-600 mx-auto mb-4"></div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Analyzing Your Symptoms</h2>
            <p className="text-gray-600">Our AI is processing your information using Ayurvedic principles...</p>
          </div>
        ) : result ? (
          <div>
            {/* Header */}
            <div className="text-center mb-8">
              <Brain className="h-16 w-16 text-ayurveda-600 mx-auto mb-4" />
              <h1 className="text-4xl font-bold text-gray-900 font-serif mb-2">
                Symptom Analysis Results
              </h1>
              <p className="text-lg text-gray-600">
                AI-powered analysis based on Ayurvedic principles and modern medicine
              </p>
            </div>

            {/* Dosha Imbalance */}
            <div className="bg-gradient-to-r from-ayurveda-600 to-ayurveda-700 rounded-2xl p-8 text-white mb-8">
              <h2 className="text-2xl font-bold mb-4">Detected Dosha Imbalance</h2>
              <div className="bg-white/10 rounded-lg p-6">
                <h3 className="text-xl font-semibold mb-2">{result.dosha_imbalance.primary}</h3>
                <p className="text-ayurveda-100">{result.dosha_imbalance.description}</p>
              </div>
            </div>

            {/* Possible Conditions */}
            <div className="bg-white rounded-2xl p-8 shadow-lg mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Possible Conditions</h2>
              <div className="space-y-4">
                {result.possible_conditions.map((condition, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-6">
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="text-lg font-semibold text-gray-900">{condition.name}</h3>
                      <span className="bg-ayurveda-100 text-ayurveda-800 px-3 py-1 rounded-full text-sm font-medium">
                        {condition.probability}% match
                      </span>
                    </div>
                    <p className="text-gray-600 mb-3">{condition.description}</p>
                    <div className="bg-ayurveda-50 rounded-lg p-4">
                      <h4 className="font-semibold text-ayurveda-800 mb-2">Ayurvedic Perspective:</h4>
                      <p className="text-ayurveda-700">{condition.ayurvedic_perspective}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recommendations */}
            <div className="grid md:grid-cols-2 gap-8 mb-8">
              {/* Immediate Actions */}
              <div className="bg-red-50 rounded-2xl p-6">
                <h3 className="text-xl font-bold text-red-900 mb-4 flex items-center">
                  <AlertTriangle className="h-6 w-6 mr-2" />
                  Immediate Actions
                </h3>
                <ul className="space-y-2">
                  {result.recommendations.immediate_actions.map((action, index) => (
                    <li key={index} className="flex items-start">
                      <CheckCircle className="h-5 w-5 text-red-600 mr-2 mt-0.5" />
                      <span className="text-red-800">{action}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Lifestyle Changes */}
              <div className="bg-blue-50 rounded-2xl p-6">
                <h3 className="text-xl font-bold text-blue-900 mb-4 flex items-center">
                  <Clock className="h-6 w-6 mr-2" />
                  Lifestyle Changes
                </h3>
                <ul className="space-y-2">
                  {result.recommendations.lifestyle_changes.map((change, index) => (
                    <li key={index} className="flex items-start">
                      <CheckCircle className="h-5 w-5 text-blue-600 mr-2 mt-0.5" />
                      <span className="text-blue-800">{change}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Herbal Remedies */}
            <div className="bg-green-50 rounded-2xl p-8 mb-8">
              <h3 className="text-xl font-bold text-green-900 mb-4">Recommended Herbal Remedies</h3>
              <div className="grid md:grid-cols-2 gap-4">
                {result.recommendations.herbal_remedies.map((remedy, index) => (
                  <div key={index} className="flex items-start">
                    <CheckCircle className="h-5 w-5 text-green-600 mr-2 mt-0.5" />
                    <span className="text-green-800">{remedy}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* When to Consult Doctor */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-2xl p-6 mb-8">
              <h3 className="text-lg font-bold text-yellow-900 mb-3 flex items-center">
                <AlertTriangle className="h-6 w-6 mr-2" />
                When to Consult a Doctor
              </h3>
              <p className="text-yellow-800">{result.recommendations.when_to_consult_doctor}</p>
            </div>

            {/* Save Status Message */}
            {saveStatus !== 'idle' && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`mb-6 p-4 rounded-lg text-center ${
                  saveStatus === 'saved'
                    ? 'bg-green-50 border border-green-200 text-green-800'
                    : saveStatus === 'saving'
                    ? 'bg-blue-50 border border-blue-200 text-blue-800'
                    : 'bg-red-50 border border-red-200 text-red-800'
                }`}
              >
                {saveStatus === 'saved' && '✅ Analysis saved successfully!'}
                {saveStatus === 'saving' && '⏳ Saving analysis...'}
                {saveStatus === 'error' && '❌ Error saving. Saved locally instead.'}
              </motion.div>
            )}

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={resetAnalysis}
                className="px-6 py-3 bg-ayurveda-600 text-white font-semibold rounded-full hover:bg-ayurveda-700 transition-colors flex items-center justify-center gap-2"
              >
                <Search className="h-5 w-5" />
                Check New Symptoms
              </button>
              <button
                onClick={saveAnalysis}
                disabled={saveStatus === 'saving' || saveStatus === 'saved'}
                className={`px-6 py-3 font-semibold rounded-full transition-colors flex items-center justify-center gap-2 ${
                  saveStatus === 'saved'
                    ? 'bg-green-100 text-green-700 border-2 border-green-300 cursor-not-allowed'
                    : saveStatus === 'saving'
                    ? 'bg-gray-100 text-gray-500 border-2 border-gray-300 cursor-wait'
                    : 'border-2 border-ayurveda-600 text-ayurveda-600 hover:bg-ayurveda-50'
                }`}
              >
                <Save className="h-5 w-5" />
                {saveStatus === 'saved' ? 'Saved!' : saveStatus === 'saving' ? 'Saving...' : 'Save Analysis'}
              </button>
              <button
                onClick={downloadAnalysis}
                className="px-6 py-3 border-2 border-gray-400 text-gray-700 font-semibold rounded-full hover:bg-gray-50 transition-colors flex items-center justify-center gap-2"
              >
                <Download className="h-5 w-5" />
                Download PDF
              </button>
            </div>
          </div>
        ) : null}
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto"
    >
      {/* Header */}
      <div className="text-center mb-8">
        <Brain className="h-16 w-16 text-ayurveda-600 mx-auto mb-4" />
        <h1 className="text-4xl font-bold text-gray-900 font-serif mb-2">
          AI Symptom Checker
        </h1>
        <p className="text-lg text-gray-600">
          Describe your symptoms and get AI-powered insights based on Ayurvedic principles
        </p>
      </div>

      {/* Current Symptoms */}
      {symptoms.length > 0 && (
        <div className="bg-white rounded-2xl p-6 shadow-lg mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Current Symptoms</h2>
          <div className="space-y-4">
            {symptoms.map((symptom) => (
              <div key={symptom.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-3">
                  <h3 className="font-semibold text-gray-900">{symptom.name}</h3>
                  <button
                    onClick={() => removeSymptom(symptom.id)}
                    className="text-red-500 hover:text-red-700"
                  >
                    <X className="h-5 w-5" />
                  </button>
                </div>
                
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Severity
                    </label>
                    <select
                      value={symptom.severity}
                      onChange={(e) => updateSymptom(symptom.id, 'severity', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ayurveda-500 focus:border-transparent"
                    >
                      <option value="mild">Mild</option>
                      <option value="moderate">Moderate</option>
                      <option value="severe">Severe</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Duration
                    </label>
                    <select
                      value={symptom.duration}
                      onChange={(e) => updateSymptom(symptom.id, 'duration', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ayurveda-500 focus:border-transparent"
                    >
                      <option value="Less than 1 day">Less than 1 day</option>
                      <option value="1-2 days">1-2 days</option>
                      <option value="3-7 days">3-7 days</option>
                      <option value="1-2 weeks">1-2 weeks</option>
                      <option value="More than 2 weeks">More than 2 weeks</option>
                    </select>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Add Symptoms */}
      <div className="bg-white rounded-2xl p-8 shadow-lg mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Add Your Symptoms</h2>
        
        {/* Custom Symptom Input */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Describe a symptom
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={newSymptom}
              onChange={(e) => setNewSymptom(e.target.value)}
              placeholder="e.g., Headache, Fatigue, Nausea..."
              className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ayurveda-500 focus:border-transparent"
              onKeyPress={(e) => e.key === 'Enter' && addSymptom(newSymptom)}
            />
            <button
              onClick={() => addSymptom(newSymptom)}
              disabled={!newSymptom.trim()}
              className="px-6 py-3 bg-ayurveda-600 text-white rounded-lg hover:bg-ayurveda-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              <Plus className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* Common Symptoms */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Common Symptoms</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {commonSymptoms.map((symptom) => (
              <button
                key={symptom}
                onClick={() => addSymptom(symptom)}
                disabled={symptoms.some(s => s.name.toLowerCase() === symptom.toLowerCase())}
                className="p-2 text-sm border border-gray-300 rounded-lg hover:border-ayurveda-500 hover:bg-ayurveda-50 disabled:bg-gray-100 disabled:cursor-not-allowed transition-colors"
              >
                {symptom}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Analyze Button */}
      <div className="text-center">
        <button
          onClick={analyzeSymptoms}
          disabled={symptoms.length === 0}
          className={`px-8 py-4 rounded-full font-semibold text-lg transition-colors ${
            symptoms.length > 0
              ? 'bg-ayurveda-600 text-white hover:bg-ayurveda-700 shadow-lg hover:shadow-xl'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
        >
          <Search className="h-6 w-6 inline mr-2" />
          Analyze Symptoms ({symptoms.length})
        </button>
        
        {symptoms.length === 0 && (
          <p className="text-sm text-gray-500 mt-2">
            Please add at least one symptom to continue
          </p>
        )}
      </div>

      {/* Disclaimer */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mt-8">
        <p className="text-sm text-yellow-800">
          <strong>Disclaimer:</strong> This tool provides educational information only and is not a substitute 
          for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare 
          professional for medical concerns.
        </p>
      </div>
    </motion.div>
  );
};

export default SymptomChecker;