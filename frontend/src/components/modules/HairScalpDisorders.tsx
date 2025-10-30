import React, { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { 
  Upload, 
  X, 
  Image as ImageIcon, 
  AlertTriangle, 
  CheckCircle, 
  Info,
  Download,
  Share2,
  Printer,
  ExternalLink,
  Activity,
  Thermometer,
  Clock,
  Target
} from 'lucide-react';
import axios from 'axios';
import YouTubeVideos from '../YouTubeVideos';

const API_URL = (process.env.REACT_APP_API_URL || 'http://localhost:8000').replace(/\/$/, '');

interface Symptom {
  id: string;
  name: string;
  severity: 'mild' | 'moderate' | 'severe';
  duration: string;
}

interface AnalysisResult {
  // Old/demo shape fields (optional now)
  detected_condition: string;
  confidence: number;
  severity: string;
  dosha_mapping?: {
    primary_dosha: string;
    imbalance_type?: string;
    description?: string;
  };
  ayurvedic_analysis?: {
    condition_type?: string;
    root_cause?: string;
    affected_doshas?: string[];
  };
  recommendations?: {
    immediate_care?: string[];
    lifestyle_changes?: string[];
    herbal_remedies?: string[];
    dietary_suggestions?: string[];
  };
  when_to_consult_doctor?: string;
  follow_up_timeline?: string;

  // New backend shape fields (optional)
  dosha_association?: string;
  ayurvedic_recommendations?: {
    herbs_oils?: string[];
    home_care?: string[];
    diet?: string[];
    lifestyle?: string[];
  };
  when_to_consult?: string;
  explainability?: string;
  disclaimer?: string;
}

const HairScalpDisorders: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [symptoms, setSymptoms] = useState<Symptom[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [availableConditions, setAvailableConditions] = useState<string[]>([]);
  const [showConditions, setShowConditions] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const commonSymptoms = [
    'Hair loss/thinning',
    'Dandruff',
    'Itchy scalp',
    'Dry scalp',
    'Oily scalp',
    'Scalp irritation',
    'Brittle hair',
    'Premature graying',
    'Hair breakage',
    'Scalp redness',
    'Flaking',
    'Burning sensation'
  ];

  const severityLevels: Array<'mild' | 'moderate' | 'severe'> = ['mild', 'moderate', 'severe'];
  const durationOptions = [
    'Less than 1 week',
    '1-2 weeks', 
    '2-4 weeks',
    '1-3 months',
    'More than 3 months'
  ];

  React.useEffect(() => {
    fetchAvailableConditions();
  }, []);

  const fetchAvailableConditions = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/hair/conditions`);
      // Backend returns { conditions: [{id, name, ...}], total }
      if (Array.isArray(response.data?.conditions)) {
        setAvailableConditions(response.data.conditions.map((c: any) => c.name || c.id));
      } else if (Array.isArray(response.data?.detectable_conditions)) {
        // Fallback to older shape
        setAvailableConditions(response.data.detectable_conditions);
      } else {
        setAvailableConditions([]);
      }
    } catch (error) {
      console.error('Error fetching conditions:', error);
    }
  };

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.type.startsWith('image/')) {
        setSelectedFile(file);
        const url = URL.createObjectURL(file);
        setPreviewUrl(url);
      } else {
        alert('Please select an image file (JPG, PNG, GIF)');
      }
    }
  };

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    }
  };

  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault();
  };

  const removeFile = () => {
    setSelectedFile(null);
    setPreviewUrl('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const addSymptom = (symptomName: string) => {
    if (!symptoms.find(s => s.name === symptomName)) {
      const newSymptom: Symptom = {
        id: Date.now().toString(),
        name: symptomName,
        severity: 'mild',
        duration: '1-2 weeks'
      };
      setSymptoms([...symptoms, newSymptom]);
    }
  };

  const updateSymptom = (id: string, field: keyof Symptom, value: string) => {
    setSymptoms(symptoms.map(s => 
      s.id === id ? { ...s, [field]: value } : s
    ));
  };

  const removeSymptom = (id: string) => {
    setSymptoms(symptoms.filter(s => s.id !== id));
  };

  const analyzeHairScalp = async () => {
    // Require at least an image or at least one symptom
    if (!selectedFile && symptoms.length === 0) {
      alert('Please upload an image or add at least one symptom');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      if (selectedFile) {
        // Backend expects the field name 'file'
        formData.append('file', selectedFile);
      }
      if (symptoms.length > 0) {
        formData.append('symptoms', JSON.stringify(symptoms));
      }

      const response = await axios.post(
        `${API_URL}/api/hair/analyze`,
        formData
      );

      setResult(response.data);
    } catch (error) {
      console.error('Analysis failed:', error);
      alert('Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'mild': return 'text-green-600 bg-green-100';
      case 'moderate': return 'text-yellow-600 bg-yellow-100';
      case 'severe': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 80) return 'text-green-600 bg-green-100';
    if (confidence >= 60) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getDoshaColor = (dosha: string) => {
    switch (dosha.toLowerCase()) {
      case 'vata': return 'text-blue-600 bg-blue-100';
      case 'pitta': return 'text-orange-600 bg-orange-100';
      case 'kapha': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  if (result) {
    // Helper to download analysis as a PDF (no extra npm deps; uses CDN jsPDF)
    const handleDownload = async () => {
      const loadJsPDF = () => new Promise<void>((resolve, reject) => {
        if ((window as any).jspdf?.jsPDF) return resolve();
        const s = document.createElement('script');
        s.src = 'https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js';
        s.onload = () => resolve();
        s.onerror = () => reject(new Error('Failed to load jsPDF'));
        document.body.appendChild(s);
      });

      await loadJsPDF();
      const { jsPDF } = (window as any).jspdf;
      const doc = new jsPDF({ unit: 'pt', format: 'a4' });

      const cond = (result as any)._conditionName || result.detected_condition || 'hair_analysis';
      const primaryDosha = result.dosha_mapping?.primary_dosha ?? (result as any).dosha_association ?? 'Unknown';
      const rec = (result.ayurvedic_recommendations || {}) as any;

      const lines: string[] = [];
      lines.push('Hair & Scalp Analysis Results');
      lines.push('');
      lines.push(`Condition: ${cond}`);
      lines.push(`Confidence: ${result.confidence}%`);
      lines.push(`Severity: ${result.severity}`);
      lines.push(`Primary Dosha: ${primaryDosha}`);
      lines.push('');
      lines.push('Recommendations:');
      if (Array.isArray(rec.herbs_oils) && rec.herbs_oils.length) lines.push(`• Herbs/Oils: ${rec.herbs_oils.join(', ')}`);
      if (Array.isArray(rec.lifestyle) && rec.lifestyle.length) lines.push(`• Lifestyle: ${rec.lifestyle.join(', ')}`);
      if (Array.isArray(rec.diet) && rec.diet.length) lines.push(`• Diet: ${rec.diet.join(', ')}`);
      if (Array.isArray(rec.home_care) && rec.home_care.length) lines.push(`• Home Care: ${rec.home_care.join(', ')}`);
      const advice = (result as any).when_to_consult || (result as any).when_to_consult_doctor;
      if (advice) { lines.push(''); lines.push(`When to consult: ${advice}`); }

      // Layout
      const marginX = 48; // 0.67in
      let cursorY = 64;   // start below top
      doc.setFont('Helvetica', 'bold');
      doc.setFontSize(18);
      doc.text('Hair & Scalp Analysis Results', marginX, cursorY);
      cursorY += 24;

      doc.setFont('Helvetica', 'normal');
      doc.setFontSize(12);
      const wrap = (text: string, width: number) => (doc as any).splitTextToSize(text, width);
      const pageWidth = doc.internal.pageSize.getWidth();
      const contentWidth = pageWidth - marginX * 2;

      for (const raw of lines.slice(2)) { // skip first heading already printed
        const blocks = wrap(raw, contentWidth);
        for (const b of blocks) {
          if (cursorY > doc.internal.pageSize.getHeight() - 64) {
            doc.addPage();
            cursorY = 64;
          }
          doc.text(b, marginX, cursorY);
          cursorY += 18;
        }
      }

      const filename = `hair_analysis_${String(cond).replace(/\s+/g, '_')}.pdf`;
      doc.save(filename);
    };

    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl mx-auto"
      >
        {/* Header */}
        <div className="mb-8 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Hair & Scalp Analysis Results</h2>
          <p className="text-gray-600">AI-powered diagnosis with Ayurvedic treatment recommendations</p>
        </div>
        {(() => { /* derive a consistent condition name across backend variants */
          // @ts-ignore - accept unknown shape from backend
          const predicted = (result as any).predicted_condition as string | undefined;
          (result as any)._conditionName = result.detected_condition ?? predicted ?? '';
          return null;
        })()}

        {/* Action Buttons */}
        <div className="flex justify-between items-center mb-6">
          <button
            onClick={() => setResult(null)}
            className="flex items-center space-x-2 px-4 py-2 text-ayurveda-600 hover:text-ayurveda-800 font-medium"
          >
            <X className="h-5 w-5" />
            <span>New Analysis</span>
          </button>
          
          <div className="flex space-x-2">
            <button onClick={handleDownload} className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              <Download className="h-4 w-4" />
              <span>Download</span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Analysis Results */}
          <div className="lg:col-span-2 space-y-6">
            {/* Main Diagnosis */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <Target className="h-6 w-6 text-ayurveda-500 mr-2" />
                Detected Condition
              </h3>
              <div className="space-y-4">
                <div>
                  <h4 className="text-2xl font-bold text-gray-900">{(result as any)._conditionName || result.detected_condition}</h4>
                  <div className="flex items-center space-x-4 mt-2">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getConfidenceColor(result.confidence)}`}>
                      {result.confidence}% Confidence
                    </span>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSeverityColor(result.severity)}`}>
                      {result.severity} Severity
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Dosha Analysis */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <Activity className="h-6 w-6 text-ayurveda-500 mr-2" />
                Ayurvedic Dosha Analysis
              </h3>
              <div className="space-y-4">
                <div>
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="font-semibold text-gray-700">Primary Dosha:</span>
                    {(() => {
                      const primary = result.dosha_mapping?.primary_dosha ?? result.dosha_association ?? 'Unknown';
                      return (
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDoshaColor(primary)}`}>
                          {primary}
                        </span>
                      );
                    })()}
                  </div>
                  {(result.dosha_mapping?.imbalance_type || result.explainability) && (
                    <div className="mb-2">
                      <span className="font-semibold text-gray-700">Explanation:</span>
                      <span className="ml-2 text-gray-600">
                        {result.dosha_mapping?.imbalance_type || result.explainability}
                      </span>
                    </div>
                  )}
                  {result.dosha_mapping?.description && (
                    <p className="text-gray-600">{result.dosha_mapping.description}</p>
                  )}
                </div>

                {(result.ayurvedic_analysis?.condition_type || result.ayurvedic_analysis?.root_cause) && (
                  <div className="border-t pt-4">
                    <h4 className="font-semibold text-gray-700 mb-2">Root Cause Analysis</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {result.ayurvedic_analysis?.condition_type && (
                        <div>
                          <span className="font-medium text-gray-600">Condition Type:</span>
                          <p className="text-gray-800">{result.ayurvedic_analysis?.condition_type}</p>
                        </div>
                      )}
                      {result.ayurvedic_analysis?.root_cause && (
                        <div>
                          <span className="font-medium text-gray-600">Root Cause:</span>
                          <p className="text-gray-800">{result.ayurvedic_analysis?.root_cause}</p>
                        </div>
                      )}
                    </div>
                    {Array.isArray(result.ayurvedic_analysis?.affected_doshas) && result.ayurvedic_analysis!.affected_doshas!.length > 0 && (
                      <div className="mt-2">
                        <span className="font-medium text-gray-600">Affected Doshas:</span>
                        <div className="flex flex-wrap gap-2 mt-1">
                          {result.ayurvedic_analysis!.affected_doshas!.map((dosha, index) => (
                            <span key={index} className={`px-2 py-1 rounded text-sm ${getDoshaColor(dosha)}`}>
                              {dosha}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* Treatment Recommendations */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <CheckCircle className="h-6 w-6 text-ayurveda-500 mr-2" />
                Ayurvedic Treatment Plan
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* If new backend shape present */}
                {result.ayurvedic_recommendations ? (
                  <>
                    <div>
                      <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                        <ImageIcon className="h-4 w-4 text-green-500 mr-2" />
                        Herbal Oils & Remedies
                      </h4>
                      <ul className="space-y-2">
                        {(result.ayurvedic_recommendations.herbs_oils || []).map((item, index) => (
                          <li key={index} className="flex items-start">
                            <CheckCircle className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-600">{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                        <Activity className="h-4 w-4 text-blue-500 mr-2" />
                        Lifestyle Changes
                      </h4>
                      <ul className="space-y-2">
                        {(result.ayurvedic_recommendations.lifestyle || []).map((item, index) => (
                          <li key={index} className="flex items-start">
                            <CheckCircle className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-600">{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                        <Thermometer className="h-4 w-4 text-orange-500 mr-2" />
                        Dietary Suggestions
                      </h4>
                      <ul className="space-y-2">
                        {(result.ayurvedic_recommendations.diet || []).map((item, index) => (
                          <li key={index} className="flex items-start">
                            <CheckCircle className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-600">{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                        <Info className="h-4 w-4 text-ayurveda-500 mr-2" />
                        Home Care
                      </h4>
                      <ul className="space-y-2">
                        {(result.ayurvedic_recommendations.home_care || []).map((item, index) => (
                          <li key={index} className="flex items-start">
                            <CheckCircle className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-600">{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </>
                ) : (
                  // Fallback to old/demo shape
                  <>
                    <div>
                      <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                        <AlertTriangle className="h-4 w-4 text-red-500 mr-2" />
                        Immediate Care
                      </h4>
                      <ul className="space-y-2">
                        {(result.recommendations?.immediate_care || []).map((item, index) => (
                          <li key={index} className="flex items-start">
                            <CheckCircle className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-600">{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                        <Activity className="h-4 w-4 text-blue-500 mr-2" />
                        Lifestyle Changes
                      </h4>
                      <ul className="space-y-2">
                        {(result.recommendations?.lifestyle_changes || []).map((item, index) => (
                          <li key={index} className="flex items-start">
                            <CheckCircle className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-600">{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                        <ImageIcon className="h-4 w-4 text-green-500 mr-2" />
                        Herbal Remedies
                      </h4>
                      <ul className="space-y-2">
                        {(result.recommendations?.herbal_remedies || []).map((item, index) => (
                          <li key={index} className="flex items-start">
                            <CheckCircle className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-600">{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                        <Thermometer className="h-4 w-4 text-orange-500 mr-2" />
                        Dietary Suggestions
                      </h4>
                      <ul className="space-y-2">
                        {(result.recommendations?.dietary_suggestions || []).map((item, index) => (
                          <li key={index} className="flex items-start">
                            <CheckCircle className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-600">{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </>
                )}
              </div>
            </div>

            {/* YouTube Videos Section */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <YouTubeVideos 
                // Use derived condition name to avoid undefined.trim()
                condition={(result as any)._conditionName || ''}
                maxResults={5}
                showEmbeddedPlayer={true}
              />
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Uploaded Image */}
            {previewUrl && (
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Analyzed Image</h3>
                <img 
                  src={previewUrl} 
                  alt="Hair/Scalp analysis" 
                  className="w-full h-48 object-cover rounded-lg"
                />
              </div>
            )}

            {/* Medical Advisory */}
            <div className="bg-red-50 border border-red-200 rounded-2xl p-6">
              <h3 className="text-lg font-semibold text-red-800 mb-2 flex items-center">
                <AlertTriangle className="h-5 w-5 mr-2" />
                When to Consult a Doctor
              </h3>
              <p className="text-red-700 text-sm mb-3">{result.when_to_consult || result.when_to_consult_doctor || 'If symptoms persist > 4 weeks or severe signs present.'}</p>
              
              {(result.follow_up_timeline) && (
                <div className="mb-3">
                  <span className="font-semibold text-red-800 flex items-center mb-1">
                    <Clock className="h-4 w-4 mr-1" />
                    Follow-up Timeline
                  </span>
                  <p className="text-red-700 text-sm">{result.follow_up_timeline}</p>
                </div>
              )}
            </div>

            {/* Additional Actions */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-lg font-semibold mb-4">Additional Resources</h3>
              <div className="space-y-3">
                <button className="w-full flex items-center space-x-2 p-3 text-left bg-ayurveda-50 hover:bg-ayurveda-100 rounded-lg transition-colors">
                  <ExternalLink className="h-4 w-4 text-ayurveda-600" />
                  <span className="text-ayurveda-700">Complete Dosha Analysis</span>
                </button>
                <button className="w-full flex items-center space-x-2 p-3 text-left bg-ayurveda-50 hover:bg-ayurveda-100 rounded-lg transition-colors">
                  <ExternalLink className="h-4 w-4 text-ayurveda-600" />
                  <span className="text-ayurveda-700">Find Ayurvedic Practitioners</span>
                </button>
                <button className="w-full flex items-center space-x-2 p-3 text-left bg-ayurveda-50 hover:bg-ayurveda-100 rounded-lg transition-colors">
                  <ExternalLink className="h-4 w-4 text-ayurveda-600" />
                  <span className="text-ayurveda-700">Learn About Hair Care</span>
                </button>
              </div>
            </div>
          </div>
        </div>
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
      <div className="mb-8 text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Hair & Scalp Disorder Analysis</h2>
        <p className="text-gray-600">Upload an image and get AI-powered diagnosis with Ayurvedic treatment recommendations</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Analysis Panel */}
        <div className="lg:col-span-2">
          {/* Image Upload Section */}
          <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
            <h3 className="text-xl font-semibold mb-4 flex items-center">
              <Upload className="h-6 w-6 text-ayurveda-500 mr-2" />
              Upload Hair/Scalp Image
            </h3>

            {!selectedFile ? (
              <div
                className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-ayurveda-400 transition-colors cursor-pointer"
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={() => fileInputRef.current?.click()}
              >
                <ImageIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <p className="text-lg font-medium text-gray-700 mb-2">
                  Drop your image here or click to browse
                </p>
                <p className="text-sm text-gray-500 mb-4">
                  Supports JPG, PNG, GIF up to 10MB
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  className="hidden"
                />
                <div className="bg-ayurveda-600 text-white px-4 py-2 rounded-lg inline-block text-sm shadow hover:bg-ayurveda-700">
                  Choose Image
                </div>
              </div>
            ) : (
              <div className="relative">
                <img 
                  src={previewUrl} 
                  alt="Selected hair/scalp" 
                  className="w-full h-64 object-cover rounded-xl"
                />
                <button
                  onClick={removeFile}
                  className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-2 hover:bg-red-600"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            )}
          </div>

          {/* Optional Symptoms Section */}
          <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
            <h3 className="text-xl font-semibold mb-4 flex items-center">
              <Info className="h-6 w-6 text-ayurveda-500 mr-2" />
              Additional Symptoms (Optional)
            </h3>
            
            <div className="mb-4">
              <p className="text-gray-600 mb-3">Select any additional symptoms you're experiencing:</p>
              <div className="flex flex-wrap gap-2">
                {commonSymptoms.map((symptom) => (
                  <button
                    key={symptom}
                    onClick={() => addSymptom(symptom)}
                    disabled={symptoms.some(s => s.name === symptom)}
                    className="px-3 py-1 border border-gray-300 rounded-full text-sm hover:bg-ayurveda-50 hover:border-ayurveda-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    {symptom}
                  </button>
                ))}
              </div>
            </div>

            {symptoms.length > 0 && (
              <div className="space-y-3">
                <h4 className="font-semibold text-gray-700">Your Symptoms:</h4>
                {symptoms.map((symptom) => (
                  <div key={symptom.id} className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
                    <div className="flex-1">
                      <span className="font-medium text-gray-800">{symptom.name}</span>
                    </div>
                    <select
                      value={symptom.severity}
                      onChange={(e) => updateSymptom(symptom.id, 'severity', e.target.value)}
                      className="border border-gray-300 rounded px-2 py-1 text-sm"
                    >
                      {severityLevels.map(level => (
                        <option key={level} value={level}>{level}</option>
                      ))}
                    </select>
                    <select
                      value={symptom.duration}
                      onChange={(e) => updateSymptom(symptom.id, 'duration', e.target.value)}
                      className="border border-gray-300 rounded px-2 py-1 text-sm"
                    >
                      {durationOptions.map(duration => (
                        <option key={duration} value={duration}>{duration}</option>
                      ))}
                    </select>
                    <button
                      onClick={() => removeSymptom(symptom.id)}
                      className="text-red-500 hover:text-red-700"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Analyze Button */}
          <button
            onClick={analyzeHairScalp}
            disabled={(!selectedFile && symptoms.length === 0) || loading}
            className="w-full bg-ayurveda-600 text-white font-semibold py-4 px-6 rounded-xl hover:bg-ayurveda-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Activity className="h-5 w-5" />
                <span>Analyze Hair & Scalp</span>
              </>
            )}
          </button>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Information Panel */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-4 text-ayurveda-800">How It Works</h3>
            <div className="space-y-3">
              <div className="flex items-start space-x-3">
                <div className="bg-ayurveda-100 text-ayurveda-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-semibold">1</div>
                <p className="text-sm text-gray-600">Upload a clear photo of the affected area</p>
              </div>
              <div className="flex items-start space-x-3">
                <div className="bg-ayurveda-100 text-ayurveda-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-semibold">2</div>
                <p className="text-sm text-gray-600">Add any additional symptoms (optional)</p>
              </div>
              <div className="flex items-start space-x-3">
                <div className="bg-ayurveda-100 text-ayurveda-600 rounded-full w-6 h-6 flex items-center justify-center text-sm font-semibold">3</div>
                <p className="text-sm text-gray-600">Get AI-powered analysis with Ayurvedic remedies</p>
              </div>
            </div>
          </div>

          {/* Detectable Conditions */}
          {availableConditions.length > 0 && (
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-lg font-semibold mb-4 text-ayurveda-800">Detectable Conditions</h3>
              <button
                onClick={() => setShowConditions(!showConditions)}
                className="text-sm text-ayurveda-600 hover:text-ayurveda-800 font-medium mb-3"
              >
                {showConditions ? 'Hide' : 'Show'} ({availableConditions.length} conditions)
              </button>
              {showConditions && (
                <div className="space-y-1">
                  {availableConditions.map((condition, index) => (
                    <div key={index} className="text-sm text-gray-600 flex items-center">
                      <CheckCircle className="h-3 w-3 text-green-500 mr-2" />
                      {condition}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Disclaimer */}
          <div className="bg-amber-50 border border-amber-200 rounded-2xl p-6">
            <h3 className="text-lg font-semibold text-amber-800 mb-2 flex items-center">
              <AlertTriangle className="h-5 w-5 mr-2" />
              Medical Disclaimer
            </h3>
            <p className="text-amber-700 text-sm">
              This AI analysis is for educational purposes only and should not replace professional medical advice. 
              Always consult qualified healthcare practitioners for proper diagnosis and treatment.
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default HairScalpDisorders;