import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { MessageCircle, Send, Bot, User } from 'lucide-react';

interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

const HealthcareChatbot: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      text: 'Namaste! I am your Ayurvedic health assistant. I can help you with health queries, provide first aid guidance, and suggest natural remedies based on Ayurvedic principles. How may I assist you today?',
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const quickQuestions = [
    "What are the three doshas in Ayurveda?",
    "How can I improve my digestion naturally?",
    "What are some home remedies for common cold?",
    "How to manage stress using Ayurvedic methods?",
    "What foods should I eat for better immunity?",
    "How to establish a daily routine according to Ayurveda?"
  ];

  const getBotResponse = (userMessage: string): string => {
    const message = userMessage.toLowerCase();
    
    if (message.includes('dosha') || message.includes('vata') || message.includes('pitta') || message.includes('kapha')) {
      return "The three doshas in Ayurveda are Vata (air & space), Pitta (fire & water), and Kapha (earth & water). Each person has a unique combination of these doshas that determines their constitution and health tendencies. Understanding your dosha helps in making appropriate dietary and lifestyle choices for optimal health.";
    }
    
    if (message.includes('digestion') || message.includes('stomach') || message.includes('gas') || message.includes('bloating')) {
      return "For better digestion according to Ayurveda: 1) Eat in a calm environment without distractions 2) Drink warm water with meals 3) Include digestive spices like ginger, cumin, and fennel 4) Eat your largest meal at midday when digestive fire is strongest 5) Take a short walk after meals 6) Avoid cold drinks with food. Would you like specific remedies for any digestive issues?";
    }
    
    if (message.includes('cold') || message.includes('cough') || message.includes('fever')) {
      return "For common cold relief: 1) Drink warm water with honey and ginger 2) Gargle with warm salt water 3) Steam inhalation with eucalyptus oil 4) Rest and stay warm 5) Drink tulsi (holy basil) tea 6) Take turmeric milk before bed. If symptoms persist beyond 7 days or worsen, please consult a healthcare provider.";
    }
    
    if (message.includes('stress') || message.includes('anxiety') || message.includes('worry')) {
      return "Ayurvedic stress management includes: 1) Practice Pranayama (breathing exercises) - especially alternate nostril breathing 2) Regular meditation or yoga 3) Abhyanga (self-massage with warm oil) 4) Maintain regular sleep schedule 5) Consume Ashwagandha or Brahmi herbs (consult practitioner) 6) Follow a Vata-pacifying diet with warm, cooked foods. What specific stress symptoms are you experiencing?";
    }
    
    if (message.includes('immunity') || message.includes('immune') || message.includes('health')) {
      return "To boost immunity naturally: 1) Include immune-boosting spices: turmeric, ginger, black pepper 2) Eat seasonal fruits and vegetables 3) Take Chyawanprash (if suitable for your constitution) 4) Practice yoga and pranayama daily 5) Get adequate sleep (7-8 hours) 6) Stay hydrated with warm water 7) Reduce processed foods and sugar. A strong digestive fire (Agni) is key to good immunity!";
    }
    
    if (message.includes('routine') || message.includes('daily') || message.includes('schedule')) {
      return "Ideal Ayurvedic daily routine (Dinacharya): Wake up before sunrise → Morning elimination → Oil pulling → Exercise/Yoga → Shower → Meditation → Breakfast → Work → Lunch (largest meal) → Brief rest → Afternoon work → Light dinner before sunset → Evening practices → Early sleep. This aligns your body with natural rhythms for optimal health.";
    }
    
    if (message.includes('headache') || message.includes('pain')) {
      return "For headaches, try: 1) Apply peppermint or eucalyptus oil to temples 2) Drink ginger tea 3) Practice gentle neck stretches 4) Apply warm compress for tension headaches, cold for migraines 5) Ensure adequate hydration 6) Practice deep breathing. If headaches are severe or persistent, please consult a doctor.";
    }
    
    if (message.includes('sleep') || message.includes('insomnia')) {
      return "For better sleep: 1) No screens 1 hour before bed 2) Warm milk with a pinch of nutmeg 3) Gentle self-massage with sesame oil 4) Practice meditation or gentle yoga 5) Keep bedroom cool and dark 6) Go to bed by 10 PM 7) Avoid heavy meals close to bedtime. Consistent sleep routine is crucial for balancing all doshas.";
    }
    
    // Default responses
    const defaultResponses = [
      "Thank you for your question. Based on Ayurvedic principles, I recommend consulting with a qualified Ayurvedic practitioner for personalized advice. In the meantime, focus on maintaining a balanced lifestyle with regular meals, adequate sleep, and stress management.",
      "That's an interesting health concern. Ayurveda emphasizes prevention through lifestyle and diet. I suggest maintaining regular routines, eating fresh and seasonal foods, and practicing mindfulness. For specific conditions, please consult a healthcare professional.",
      "I appreciate you sharing this with me. Ayurveda teaches us that each person is unique. While I can provide general guidance, I recommend personalized consultation for your specific needs. Would you like to know about any particular Ayurvedic practices or principles?"
    ];
    
    return defaultResponses[Math.floor(Math.random() * defaultResponses.length)];
  };

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Simulate API call delay
    setTimeout(() => {
      const botResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: getBotResponse(inputMessage),
        sender: 'bot',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 1500);
  };

  const sendQuickQuestion = (question: string) => {
    setInputMessage(question);
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto h-[80vh] flex flex-col"
    >
      {/* Header */}
      <div className="text-center mb-6">
        <MessageCircle className="h-16 w-16 text-ayurveda-600 mx-auto mb-4" />
        <h1 className="text-4xl font-bold text-gray-900 font-serif mb-2">
          Healthcare Chatbot
        </h1>
        <p className="text-lg text-gray-600">
          Get instant Ayurvedic guidance and first aid measures from our AI assistant
        </p>
      </div>

      <div className="bg-white rounded-2xl shadow-lg flex-1 flex flex-col overflow-hidden">
        {/* Chat Messages */}
        <div className="flex-1 p-6 overflow-y-auto space-y-4">
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl ${
                  message.sender === 'user'
                    ? 'bg-ayurveda-600 text-white'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                <div className="flex items-start space-x-2">
                  {message.sender === 'bot' && (
                    <Bot className="h-5 w-5 text-ayurveda-600 mt-0.5 flex-shrink-0" />
                  )}
                  {message.sender === 'user' && (
                    <User className="h-5 w-5 text-white mt-0.5 flex-shrink-0 order-2" />
                  )}
                  <div className="flex-1">
                    <p className="text-sm leading-relaxed">{message.text}</p>
                    <p
                      className={`text-xs mt-1 ${
                        message.sender === 'user' ? 'text-ayurveda-200' : 'text-gray-500'
                      }`}
                    >
                      {formatTime(message.timestamp)}
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
          
          {isTyping && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-start"
            >
              <div className="bg-gray-100 text-gray-800 px-4 py-3 rounded-2xl">
                <div className="flex items-center space-x-2">
                  <Bot className="h-5 w-5 text-ayurveda-600" />
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Questions */}
        {messages.length <= 1 && (
          <div className="px-6 py-4 border-t border-gray-200">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Quick Questions:</h3>
            <div className="flex flex-wrap gap-2">
              {quickQuestions.slice(0, 3).map((question, index) => (
                <button
                  key={index}
                  onClick={() => sendQuickQuestion(question)}
                  className="text-xs px-3 py-2 bg-ayurveda-100 text-ayurveda-800 rounded-full hover:bg-ayurveda-200 transition-colors"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Message Input */}
        <div className="p-6 border-t border-gray-200">
          <div className="flex space-x-4">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
              placeholder="Ask about health, symptoms, or Ayurvedic remedies..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-full focus:ring-2 focus:ring-ayurveda-500 focus:border-transparent"
              disabled={isTyping}
            />
            <button
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isTyping}
              className="px-6 py-3 bg-ayurveda-600 text-white rounded-full hover:bg-ayurveda-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="h-5 w-5" />
            </button>
          </div>
          
          <p className="text-xs text-gray-500 mt-2 text-center">
            This chatbot provides general information only. For medical emergencies, contact emergency services immediately.
          </p>
        </div>
      </div>
    </motion.div>
  );
};

export default HealthcareChatbot;