import React, { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { Shield, Upload, Camera, AlertTriangle, CheckCircle } from 'lucide-react';
import YouTubeVideos from '../YouTubeVideos';

interface SkinAnalysisResult {
  detected_condition: string;
  confidence: number;
  description: string;
  ayurvedic_treatment: {
    herbal_remedies: string[];
    dietary_recommendations: string[];
    lifestyle_changes: string[];
  };
  severity: 'mild' | 'moderate' | 'severe';
  when_to_consult_doctor: string;
}

const SkinDiseaseDetection: React.FC = () => {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SkinAnalysisResult | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setSelectedImage(e.target?.result as string);
        setResult(null);
      };
      reader.readAsDataURL(file);
    }
  };

  const analyzeImage = async () => {
    if (!selectedImage || !selectedFile) return;
    
    setLoading(true);
    
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      
      const response = await fetch('http://localhost:8000/api/skin/analyze', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }
      
      const data: SkinAnalysisResult = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error analyzing image:', error);
      alert('Failed to analyze image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    setSelectedImage(null);
    setSelectedFile(null);
    setResult(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto"
    >
      {/* Header */}
      <div className="text-center mb-8">
        <Shield className="h-16 w-16 text-ayurveda-600 mx-auto mb-4" />
        <h1 className="text-4xl font-bold text-gray-900 font-serif mb-2">
          Skin Disease Detection
        </h1>
        <p className="text-lg text-gray-600">
          Upload an image for CNN-based analysis and receive Ayurvedic treatment recommendations
        </p>
      </div>

      {result ? (
        /* Results Display */
        <div>
          <div className="bg-white rounded-2xl p-8 shadow-lg mb-8">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Analysis Results</h2>
              <button
                onClick={async () => {
                  // lazy-load jsPDF
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
                  const marginX = 48;
                  let y = 64;
                  // Title
                  doc.setFont('Helvetica','bold');
                  doc.setFontSize(18);
                  doc.text('Skin Disease Analysis Results', marginX, y); y += 24;
                  // Info
                  doc.setFont('Helvetica','normal');
                  doc.setFontSize(12);
                  const wrap = (t: string, w: number) => (doc as any).splitTextToSize(t, w);
                  const pageW = doc.internal.pageSize.getWidth();
                  const width = pageW - marginX*2;
                  const add = (text: string) => {
                    const lines = wrap(text, width);
                    for (const l of lines) {
                      if (y > doc.internal.pageSize.getHeight()-64) { doc.addPage(); y = 64; }
                      doc.text(l, marginX, y); y += 18;
                    }
                  };
                  add(`Condition: ${result.detected_condition}`);
                  add(`Confidence: ${result.confidence}%`);
                  add(`Severity: ${result.severity}`);
                  add('');
                  add('Description:');
                  add(result.description);
                  add('');
                  add('Recommendations:');
                  if (result.ayurvedic_treatment.herbal_remedies?.length) add(`• Herbal Remedies: ${result.ayurvedic_treatment.herbal_remedies.join(', ')}`);
                  if (result.ayurvedic_treatment.dietary_recommendations?.length) add(`• Diet: ${result.ayurvedic_treatment.dietary_recommendations.join(', ')}`);
                  if (result.ayurvedic_treatment.lifestyle_changes?.length) add(`• Lifestyle: ${result.ayurvedic_treatment.lifestyle_changes.join(', ')}`);
                  add('');
                  add(`When to consult: ${result.when_to_consult_doctor}`);
                  const fname = `skin_analysis_${result.detected_condition.replace(/\s+/g,'_')}.pdf`;
                  doc.save(fname);
                }}
                className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4"><path d="M12 16a1 1 0 0 0 .707-.293l4-4-1.414-1.414L13 12.586V3h-2v9.586L8.707 10.293 7.293 11.707l4 4A1 1 0 0 0 12 16z"/><path d="M5 18h14v2H5z"/></svg>
                <span>Download</span>
              </button>
            </div>
            
            <div className="grid md:grid-cols-2 gap-8 mb-8">
              <div>
                <img 
                  src={selectedImage!} 
                  alt="Analyzed skin condition" 
                  className="w-full h-64 object-cover rounded-lg"
                />
              </div>
              
              <div>
                <div className="bg-gradient-to-r from-ayurveda-600 to-ayurveda-700 rounded-lg p-6 text-white mb-4">
                  <h3 className="text-xl font-bold mb-2">{result.detected_condition}</h3>
                  <p className="text-ayurveda-100 mb-2">Confidence: {result.confidence}%</p>
                  <p className="text-ayurveda-100">Severity: {result.severity}</p>
                </div>
                <p className="text-gray-600">{result.description}</p>
              </div>
            </div>

            {/* Treatment Recommendations */}
            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="bg-green-50 rounded-lg p-6">
                <h3 className="text-lg font-bold text-green-900 mb-4">Herbal Remedies</h3>
                <ul className="space-y-2">
                  {result.ayurvedic_treatment.herbal_remedies.map((remedy, index) => (
                    <li key={index} className="flex items-start">
                      <CheckCircle className="h-5 w-5 text-green-600 mr-2 mt-0.5" />
                      <span className="text-green-800 text-sm">{remedy}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-blue-50 rounded-lg p-6">
                <h3 className="text-lg font-bold text-blue-900 mb-4">Dietary Recommendations</h3>
                <ul className="space-y-2">
                  {result.ayurvedic_treatment.dietary_recommendations.map((diet, index) => (
                    <li key={index} className="flex items-start">
                      <CheckCircle className="h-5 w-5 text-blue-600 mr-2 mt-0.5" />
                      <span className="text-blue-800 text-sm">{diet}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-purple-50 rounded-lg p-6">
                <h3 className="text-lg font-bold text-purple-900 mb-4">Lifestyle Changes</h3>
                <ul className="space-y-2">
                  {result.ayurvedic_treatment.lifestyle_changes.map((lifestyle, index) => (
                    <li key={index} className="flex items-start">
                      <CheckCircle className="h-5 w-5 text-purple-600 mr-2 mt-0.5" />
                      <span className="text-purple-800 text-sm">{lifestyle}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Doctor Consultation Warning */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-8">
              <h3 className="text-lg font-bold text-yellow-900 mb-3 flex items-center">
                <AlertTriangle className="h-6 w-6 mr-2" />
                When to Consult a Doctor
              </h3>
              <p className="text-yellow-800">{result.when_to_consult_doctor}</p>
            </div>

            <div className="text-center">
              <button
                onClick={resetAnalysis}
                className="px-6 py-3 bg-ayurveda-600 text-white font-semibold rounded-full hover:bg-ayurveda-700 transition-colors"
              >
                Analyze Another Image
              </button>
            </div>
          </div>

          {/* YouTube Videos Section */}
          <div className="bg-white rounded-2xl p-8 shadow-lg">
            <YouTubeVideos 
              condition={result.detected_condition}
              maxResults={5}
              showEmbeddedPlayer={true}
            />
          </div>
        </div>
      ) : (
        /* Upload Interface */
        <div>
          <div className="bg-white rounded-2xl p-8 shadow-lg mb-8">
            {selectedImage ? (
              <div>
                <div className="text-center mb-6">
                  <img 
                    src={selectedImage} 
                    alt="Selected for analysis" 
                    className="max-w-full h-64 mx-auto object-cover rounded-lg shadow-lg"
                  />
                </div>
                <div className="text-center">
                  <button
                    onClick={analyzeImage}
                    disabled={loading}
                    className="px-8 py-4 bg-ayurveda-600 text-white font-semibold rounded-full hover:bg-ayurveda-700 disabled:opacity-50 transition-colors mr-4"
                  >
                    {loading ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2 inline-block" />
                        Analyzing...
                      </>
                    ) : (
                      'Analyze Image'
                    )}
                  </button>
                  <button
                    onClick={() => setSelectedImage(null)}
                    className="px-6 py-3 border border-gray-300 text-gray-700 font-semibold rounded-full hover:bg-gray-50 transition-colors"
                  >
                    Choose Different Image
                  </button>
                </div>
              </div>
            ) : (
              <div>
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleImageUpload}
                  accept="image/*"
                  className="hidden"
                />
                
                <div 
                  onClick={() => fileInputRef.current?.click()}
                  className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center cursor-pointer hover:border-ayurveda-500 hover:bg-ayurveda-50 transition-colors"
                >
                  <Upload className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    Upload Skin Image
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Click to select an image of the affected skin area
                  </p>
                  <div className="flex justify-center space-x-4">
                    <span className="inline-flex items-center px-4 py-2 bg-ayurveda-600 text-white rounded-full text-sm">
                      <Camera className="h-4 w-4 mr-2" />
                      Choose File
                    </span>
                  </div>
                </div>
                
                <div className="mt-6 text-center text-sm text-gray-500">
                  <p>Supported formats: JPG, PNG, GIF (Max size: 10MB)</p>
                  <p className="mt-2">Our AI can detect 22 categories of skin conditions</p>
                </div>
              </div>
            )}
          </div>

          {/* Supported Conditions */}
          <div className="bg-ayurveda-50 rounded-2xl p-8">
            <h2 className="text-2xl font-bold text-ayurveda-900 mb-6 text-center">
              Detectable Skin Conditions
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              {[
                'Eczema', 'Psoriasis', 'Acne', 'Dermatitis',
                'Rosacea', 'Vitiligo', 'Fungal Infections', 'Hives',
                'Melanoma', 'Basal Cell Carcinoma', 'Warts', 'Herpes',
                'Seborrheic Dermatitis', 'Contact Dermatitis', 'Impetigo', 'Cellulitis',
                'Scabies', 'Ringworm', 'Age Spots', 'Moles',
                'Skin Tags', 'Keratosis'
              ].map((condition) => (
                <div key={condition} className="bg-white rounded-lg p-3 shadow-sm">
                  <span className="text-ayurveda-800 font-medium text-sm">{condition}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Disclaimer */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mt-8">
            <p className="text-sm text-yellow-800">
              <strong>Medical Disclaimer:</strong> This AI tool is for educational and informational purposes only. 
              It should not be used as a substitute for professional medical diagnosis or treatment. Always consult 
              with a qualified dermatologist or healthcare provider for proper diagnosis and treatment of skin conditions.
            </p>
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default SkinDiseaseDetection;