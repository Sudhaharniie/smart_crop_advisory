// FIXED: Voice Synthesis with better browser support and error handling
let currentUtterance = null;

function speakText(text, lang = 'en') {
    console.log('🔊 Speaking:', text.substring(0, 50) + '...');
    
    if (!('speechSynthesis' in window)) {
        console.error('❌ Speech synthesis not supported');
        showToast('Voice feature not supported in this browser', 'error');
        return false;
    }

    try {
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();
        
        // Wait a bit for cancel to complete
        setTimeout(() => {
            const utterance = new SpeechSynthesisUtterance(text);
            
            // Enhanced language mapping
            const langMap = {
                'en': 'en-US',
                'hi': 'hi-IN',
                'bn': 'bn-IN',
                'te': 'te-IN', 
                'ta': 'ta-IN',
                'gu': 'gu-IN',
                'mr': 'mr-IN',
                'kn': 'kn-IN'
            };
            
            utterance.lang = langMap[lang] || 'en-US';
            utterance.rate = 0.9;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;
            
            // Event handlers
            utterance.onstart = () => {
                console.log('✅ Speech started');
                currentUtterance = utterance;
            };
            
            utterance.onend = () => {
                console.log('✅ Speech ended');
                currentUtterance = null;
            };
            
            utterance.onerror = (event) => {
                console.error('❌ Speech error:', event.error);
                if (event.error !== 'canceled') {
                    showToast('Voice playback error: ' + event.error, 'error');
                }
                currentUtterance = null;
            };
            
            // Speak
            window.speechSynthesis.speak(utterance);
            showToast('🔊 Playing voice...', 'info');
            
        }, 100);
        
        return true;
        
    } catch (error) {
        console.error('❌ Speech synthesis error:', error);
        showToast('Voice feature error. Try Chrome or Edge browser.', 'error');
        return false;
    }
}

function stopSpeaking() {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        currentUtterance = null;
        console.log('🛑 Speech stopped');
    }
}

function speakDashboard() {
    const lang = localStorage.getItem('preferredLanguage') || 'en';
    const texts = {
        'en': 'Welcome to Smart Crop Advisory Dashboard. View real-time weather data, soil analysis, AI crop recommendations, and live market prices. All features are powered by machine learning and government APIs.',
        'hi': 'स्मार्ट क्रॉप एडवाइजरी डैशबोर्ड में आपका स्वागत है। वास्तविक समय मौसम डेटा, मिट्टी विश्लेषण, एआई फसल सिफारिशें और लाइव बाजार मूल्य देखें।',
        'bn': 'স্মার্ট ক্রপ অ্যাডভাইজরি ড্যাশবোর্ডে স্বাগতম। রিয়েল-টাইম আবহাওয়া ডেটা, মাটি বিশ্লেষণ, এআই ফসল সুপারিশ এবং লাইভ বাজার মূল্য দেখুন।',
        'te': 'స్మార్ట్ క్రాప్ అడ్వైజరీ డాష్‌బోర్డ్‌కు స్వాగతం। రియల్-టైమ్ వాతావరణ డేటా, నేల విశ్లేషణ, AI పంట సిఫార్సులు మరియు లైవ్ మార్కెట్ ధరలను చూడండి।',
        'ta': 'ஸ்மார்ட் பயிர் ஆலோசனை டாஷ்போர்டுக்கு வரவேற்கிறோம். நிகழ்நேர வானிலை தரவு, மண் பகுப்பாய்வு, AI பயிர் பரிந்துரைகள் மற்றும் நேரடி சந்தை விலைகளைக் காண்க.'
    };
    
    const text = texts[lang] || texts['en'];
    speakText(text, lang);
}

function speakCropRecommendation() {
    const lang = localStorage.getItem('preferredLanguage') || 'en';
    
    // Get crop name from dashboard
    const cropElement = document.querySelector('.metric-crop .metric-value');
    const confidenceElement = document.querySelector('.metric-confidence .metric-value');
    const profitElement = document.querySelector('.metric-profit .metric-value');
    
    let cropName = cropElement ? cropElement.textContent.trim() : 'recommended crop';
    let confidence = confidenceElement ? confidenceElement.textContent.trim() : '90%';
    let profit = profitElement ? profitElement.textContent.trim() : 'high';
    
    const texts = {
        'en': `Top crop recommendation: ${cropName}. AI confidence score is ${confidence}. Expected profit is ${profit}. This crop has the highest profit potential for your farm based on soil and weather analysis.`,
        'hi': `शीर्ष फसल सिफारिश: ${cropName}। एआई विश्वास स्कोर ${confidence} है। अपेक्षित लाभ ${profit} है। यह फसल आपके खेत के लिए सबसे अधिक लाभ क्षमता रखती है।`,
        'bn': `শীর্ষ ফসল সুপারিশ: ${cropName}। AI আত্মবিশ্বাস স্কোর ${confidence}। প্রত্যাশিত লাভ ${profit}। এই ফসলটি আপনার খামারের জন্য সর্বোচ্চ লাভের সম্ভাবনা রয়েছে।`,
        'te': `టాప్ పంట సిఫార్సు: ${cropName}. AI విశ్వాస స్కోరు ${confidence}. ఆశించిన లాభం ${profit}. ఈ పంట మీ పొలానికి అత్యధిక లాభ సంభావ్యతను కలిగి ఉంది।`,
        'ta': `சிறந்த பயிர் பரிந்துரை: ${cropName}. AI நம்பிக்கை மதிப்பெண் ${confidence}. எதிர்பார்க்கப்படும் இலாபம் ${profit}. இந்த பயிர் உங்கள் பண்ணைக்கு அதிக லாப சாத்தியத்தைக் கொண்டுள்ளது.`
    };
    
    const text = texts[lang] || texts['en'];
    speakText(text, lang);
}

function speakWeather() {
    const lang = localStorage.getItem('preferredLanguage') || 'en';
    
    // Get weather data from dashboard
    const tempElements = document.querySelectorAll('.weather-card h3');
    let temp = tempElements[0] ? tempElements[0].textContent.trim() : '25°C';
    let humidity = tempElements[1] ? tempElements[1].textContent.trim() : '60%';
    let rainfall = tempElements[2] ? tempElements[2].textContent.trim() : '5mm';
    
    const texts = {
        'en': `Current weather conditions: Temperature is ${temp}, Humidity is ${humidity}, Rainfall is ${rainfall}. Check the 7-day weather forecast for detailed predictions and plan your farming activities accordingly.`,
        'hi': `वर्तमान मौसम की स्थिति: तापमान ${temp} है, आर्द्रता ${humidity} है, वर्षा ${rainfall} है। विस्तृत भविष्यवाणियों के लिए 7-दिवसीय मौसम पूर्वानुमान देखें।`,
        'bn': `বর্তমান আবহাওয়া পরিস্থিতি: তাপমাত্রা ${temp}, আর্দ্রতা ${humidity}, বৃষ্টিপাত ${rainfall}। বিস্তারিত পূর্বাভাসের জন্য 7-দিনের আবহাওয়া পূর্বাভাস দেখুন।`,
        'te': `ప్రస్తుత వాతావరణ పరిస్థితులు: ఉష్ణోగ్రత ${temp}, తేమ ${humidity}, వర్షపాతం ${rainfall}. వివరణాత్మక అంచనాల కోసం 7-రోజుల వాతావరణ సూచనను చూడండి।`,
        'ta': `தற்போதைய வானிலை நிலைமைகள்: வெப்பநிலை ${temp}, ஈரப்பதம் ${humidity}, மழைப்பொழிவு ${rainfall}. விரிவான கணிப்புகளுக்கு 7-நாள் வானிலை முன்னறிவிப்பைப் பார்க்கவும்.`
    };
    
    const text = texts[lang] || texts['en'];
    speakText(text, lang);
}

function speakSoilData() {
    const lang = localStorage.getItem('preferredLanguage') || 'en';
    
    const soilHealthElement = document.querySelector('.metric-soil .metric-value');
    let soilHealth = soilHealthElement ? soilHealthElement.textContent.trim() : '75%';
    
    const texts = {
        'en': `Soil health status: Your soil health score is ${soilHealth}. Monitor nitrogen, phosphorus, and potassium levels regularly for optimal crop growth. Update soil data every 3 months for accurate recommendations.`,
        'hi': `मिट्टी स्वास्थ्य स्थिति: आपका मिट्टी स्वास्थ्य स्कोर ${soilHealth} है। इष्टतम फसल वृद्धि के लिए नाइट्रोजन, फास्फोरस और पोटेशियम स्तरों की नियमित निगरानी करें।`,
        'bn': `মাটির স্বাস্থ্য অবস্থা: আপনার মাটির স্বাস্থ্য স্কোর ${soilHealth}। সর্বোত্তম ফসল বৃদ্ধির জন্য নাইট্রোজেন, ফসফরাস এবং পটাসিয়াম স্তর নিয়মিত পর্যবেক্ষণ করুন।`,
        'te': `నేల ఆరోగ్య స్థితి: మీ నేల ఆరోగ్య స్కోరు ${soilHealth}. సరైన పంట పెరుగుదల కోసం నత్రజని, భాస్వరం మరియు పొటాషియం స్థాయిలను క్రమం తప్పకుండా పర్యవేక్షించండి।`,
        'ta': `மண் ஆரோக்கிய நிலை: உங்கள் மண் ஆரோக்கிய மதிப்பெண் ${soilHealth}. உகந்த பயிர் வளர்ச்சிக்கு நைட்ரஜன், பாஸ்பரஸ் மற்றும் பொட்டாசியம் அளவுகளை தவறாமல் கண்காணிக்கவும்.`
    };
    
    const text = texts[lang] || texts['en'];
    speakText(text, lang);
}

function speakIrrigation() {
    const lang = localStorage.getItem('preferredLanguage') || 'en';
    
    const texts = {
        'en': 'Irrigation advice: Water crops based on soil moisture levels and weather forecast. Use drip irrigation to save 30% water and improve efficiency. Irrigate during early morning or late evening for best results.',
        'hi': 'सिंचाई सलाह: मिट्टी की नमी और मौसम पूर्वानुमान के आधार पर फसलों को पानी दें। 30% पानी बचाने के लिए ड्रिप सिंचाई का उपयोग करें। सर्वोत्तम परिणामों के लिए सुबह जल्दी या देर शाम सिंचाई करें।',
        'bn': 'সেচ পরামর্শ: মাটির আর্দ্রতা এবং আবহাওয়া পূর্বাভাসের উপর ভিত্তি করে ফসলে জল দিন। 30% জল সাশ্রয় করতে ড্রিপ সেচ ব্যবহার করুন। সেরা ফলাফলের জন্য ভোরে বা সন্ধ্যায় সেচ দিন।',
        'te': 'నీటిపారుదల సలహా: నేల తేమ స్థాయిలు మరియు వాతావరణ సూచన ఆధారంగా పంటలకు నీరు పెట్టండి। 30% నీటిని ఆదా చేయడానికి డ్రిప్ నీటిపారుదల ఉపయోగించండి। ఉత్తమ ఫలితాల కోసం తెల్లవారుజామున లేదా సాయంత్రం నీరు పెట్టండి।',
        'ta': 'நீர்ப்பாசன ஆலோசனை: மண் ஈரப்பதம் மற்றும் வானிலை முன்னறிவிப்பின் அடிப்படையில் பயிர்களுக்கு நீர் பாய்ச்சவும். 30% தண்ணீரை சேமிக்க சொட்டு நீர்ப்பாசனத்தைப் பயன்படுத்தவும். சிறந்த முடிவுகளுக்கு அதிகாலை அல்லது மாலை நேரத்தில் நீர் பாய்ச்சவும்.'
    };
    
    const text = texts[lang] || texts['en'];
    speakText(text, lang);
}

function speakFertilizer() {
    const lang = localStorage.getItem('preferredLanguage') || 'en';
    
    const texts = {
        'en': 'Fertilizer recommendations: Apply NPK fertilizers based on soil test results. Use Urea for nitrogen, DAP for phosphorus, and MOP for potassium. Prefer organic compost for better soil health and sustainable farming.',
        'hi': 'उर्वरक सिफारिशें: मिट्टी परीक्षण परिणामों के आधार पर एनपीके उर्वरक लागू करें। नाइट्रोजन के लिए यूरिया, फास्फोरस के लिए डीएपी, और पोटेशियम के लिए एमओपी का उपयोग करें। बेहतर मिट्टी स्वास्थ्य के लिए जैविक खाद पसंद करें।',
        'bn': 'সার সুপারিশ: মাটি পরীক্ষার ফলাফলের উপর ভিত্তি করে NPK সার প্রয়োগ করুন। নাইট্রোজেনের জন্য ইউরিয়া, ফসফরাসের জন্য DAP এবং পটাসিয়ামের জন্য MOP ব্যবহার করুন। ভাল মাটির স্বাস্থ্যের জন্য জৈব কম্পোস্ট পছন্দ করুন।',
        'te': 'ఎరువుల సిఫార్సులు: నేల పరీక్ష ఫలితాల ఆధారంగా NPK ఎరువులు వర్తించండి। నత్రజని కోసం యూరియా, భాస్వరం కోసం DAP మరియు పొటాషియం కోసం MOP ఉపయోగించండి। మెరుగైన నేల ఆరోగ్యం కోసం సేంద్రీయ కంపోస్ట్‌ను ఇష్టపడండి।',
        'ta': 'உர பரிந்துரைகள்: மண் சோதனை முடிவுகளின் அடிப்படையில் NPK உரங்களைப் பயன்படுத்தவும். நைட்ரஜனுக்கு யூரியா, பாஸ்பரஸுக்கு DAP மற்றும் பொட்டாசியத்திற்கு MOP பயன்படுத்தவும். சிறந்த மண் ஆரோக்கியத்திற்கு கரிம உரத்தை விரும்பவும்.'
    };
    
    const text = texts[lang] || texts['en'];
    speakText(text, lang);
}

function speakMarketPrices() {
    const lang = localStorage.getItem('preferredLanguage') || 'en';
    
    const texts = {
        'en': 'Market prices are updated daily from government mandi API. Check the market section for current crop prices and trends. Sell your crops when prices are trending upward for maximum profit.',
        'hi': 'बाजार मूल्य सरकारी मंडी एपीआई से दैनिक अपडेट किए जाते हैं। वर्तमान फसल मूल्यों और रुझानों के लिए बाजार अनुभाग देखें। अधिकतम लाभ के लिए जब कीमतें ऊपर की ओर हों तब अपनी फसलें बेचें।',
        'bn': 'বাজার মূল্য সরকারি মান্ডি API থেকে প্রতিদিন আপডেট করা হয়। বর্তমান ফসলের দাম এবং প্রবণতার জন্য বাজার বিভাগ দেখুন। সর্বাধিক লাভের জন্য যখন দাম বাড়ছে তখন আপনার ফসল বিক্রি করুন।',
        'te': 'మార్కెట్ ధరలు ప్రభుత్వ మండి API నుండి ప్రతిరోజూ నవీకరించబడతాయి. ప్రస్తుత పంట ధరలు మరియు ధోరణుల కోసం మార్కెట్ విభాగాన్ని చూడండి. గరిష్ట లాభం కోసం ధరలు పెరుగుతున్నప్పుడు మీ పంటలను అమ్మండి।',
        'ta': 'சந்தை விலைகள் அரசு மண்டி API இலிருந்து தினசரி புதுப்பிக்கப்படுகின்றன. தற்போதைய பயிர் விலைகள் மற்றும் போக்குகளுக்கு சந்தை பிரிவைப் பார்க்கவும். அதிகபட்ச லாபத்திற்கு விலைகள் உயரும்போது உங்கள் பயிர்களை விற்கவும்.'
    };
    
    const text = texts[lang] || texts['en'];
    speakText(text, lang);
}

// Helper function to show toast notifications
function showToast(message, type = 'info') {
    console.log(`📢 Toast: ${message} (${type})`);
    
    // Try to use existing toast system
    if (typeof window.showToast === 'function') {
        window.showToast(message, type);
        return;
    }
    
    // Fallback: create simple toast
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed bottom-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Stop speech when page unloads
window.addEventListener('beforeunload', stopSpeaking);
