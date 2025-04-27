document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            
            // Update active tab button
            tabBtns.forEach(btn => btn.classList.remove('active'));
            btn.classList.add('active');
            
            // Show the selected tab content
            tabPanes.forEach(pane => {
                pane.classList.remove('active');
                if (pane.id === tabId) {
                    pane.classList.add('active');
                }
            });
            
            // Hide response container when switching tabs
            document.getElementById('response-container').classList.add('hidden');
        });
    });
    
    // Text Query Submission
    const textQueryBtn = document.getElementById('send-text');
    textQueryBtn.addEventListener('click', async () => {
        const query = document.getElementById('text-query').value.trim();
        
        if (!query) {
            alert('Please enter a question or symptom description');
            return;
        }
        
        // Show loading state
        textQueryBtn.disabled = true;
        textQueryBtn.innerText = 'Processing...';
        
        try {
            const response = await fetch('/api/text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query })
            });
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Display response
            displayResponse(data.response);
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            // Reset button state
            textQueryBtn.disabled = false;
            textQueryBtn.innerText = 'Get Information';
        }
    });
    
    // Image Upload Preview
    const imageUpload = document.getElementById('image-upload');
    const fileNameDisplay = document.getElementById('file-name');
    const imagePreviewContainer = document.getElementById('image-preview-container');
    const imagePreview = document.getElementById('image-preview');
    const analyzeImageBtn = document.getElementById('analyze-image');
    
    imageUpload.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            fileNameDisplay.textContent = file.name;
            
            // Enable the analyze button
            analyzeImageBtn.disabled = false;
            
            // Show image preview
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                imagePreviewContainer.classList.remove('hidden');
            }
            reader.readAsDataURL(file);
        } else {
            fileNameDisplay.textContent = 'No file selected';
            analyzeImageBtn.disabled = true;
            imagePreviewContainer.classList.add('hidden');
        }
    });
    
    // Image Analysis Submission
    analyzeImageBtn.addEventListener('click', async () => {
        const imageFile = imageUpload.files[0];
        const description = document.getElementById('image-description').value;
        
        if (!imageFile) {
            alert('Please select an image to analyze');
            return;
        }
        
        // Show loading state
        analyzeImageBtn.disabled = true;
        analyzeImageBtn.innerText = 'Analyzing...';
        
        try {
            const formData = new FormData();
            formData.append('image', imageFile);
            formData.append('description', description);
            
            const response = await fetch('/api/image', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Display response
            displayResponse(data.analysis);
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            // Reset button state
            analyzeImageBtn.disabled = false;
            analyzeImageBtn.innerText = 'Analyze Image';
        }
    });
    
    // Audio Recording
    const startRecordingBtn = document.getElementById('start-recording');
    const stopRecordingBtn = document.getElementById('stop-recording');
    const recordingStatus = document.getElementById('recording-status');
    const transcriptionContainer = document.getElementById('transcription-container');
    const transcriptionText = document.getElementById('transcription-text');
    
    let mediaRecorder;
    let audioChunks = [];
    
    startRecordingBtn.addEventListener('click', async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            // Update UI
            recordingStatus.textContent = 'Recording in progress...';
            recordingStatus.style.color = '#e74c3c';
            startRecordingBtn.disabled = true;
            stopRecordingBtn.disabled = false;
            transcriptionContainer.classList.add('hidden');
            
            // Initialize media recorder
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            
            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });
            
            mediaRecorder.addEventListener('stop', async () => {
                // Stop all audio tracks
                stream.getTracks().forEach(track => track.stop());
                
                // Create audio blob and send for processing
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                await processAudioRecording(audioBlob);
            });
            
            // Start recording
            mediaRecorder.start();
        } catch (error) {
            alert('Error accessing microphone: ' + error.message);
        }
    });
    
    stopRecordingBtn.addEventListener('click', () => {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            
            // Update UI
            recordingStatus.textContent = 'Processing audio...';
            recordingStatus.style.color = '#3498db';
            stopRecordingBtn.disabled = true;
        }
    });
    
    async function processAudioRecording(audioBlob) {
        try {
            const formData = new FormData();
            formData.append('audio', audioBlob);
            
            const response = await fetch('/api/audio', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Show transcription
            transcriptionText.textContent = data.transcription;
            transcriptionContainer.classList.remove('hidden');
            
            // Display response
            displayResponse(data.response);
        } catch (error) {
            alert('Error processing audio: ' + error.message);
        } finally {
            // Reset UI
            recordingStatus.textContent = 'Not recording';
            recordingStatus.style.color = '';
            startRecordingBtn.disabled = false;
        }
    }
    
    // Display response function
    function displayResponse(response) {
        const responseContainer = document.getElementById('response-container');
        const responseContent = document.getElementById('response-content');
        
        // Format the response text with markdown-like formatting
        const formattedResponse = formatResponse(response);
        
        responseContent.innerHTML = formattedResponse;
        responseContainer.classList.remove('hidden');
        
        // Scroll to response
        responseContainer.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Format response with basic HTML formatting
    function formatResponse(text) {
        if (!text) return '';
        
        // Replace newlines with <br>
        text = text.replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>');
        
        // Wrap in paragraph tags if not already
        if (!text.startsWith('<p>')) {
            text = '<p>' + text;
        }
        if (!text.endsWith('</p>')) {
            text = text + '</p>';
        }
        
        // Bold text between ** markers
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Italics
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
    
       // Headers
       text = text.replace(/^### (.*?)$/gm, '<h5>$1</h5>');
       text = text.replace(/^## (.*?)$/gm, '<h4>$1</h4>');
       text = text.replace(/^# (.*?)$/gm, '<h3>$1</h3>');
       
       // Lists
       text = text.replace(/^\- (.*?)$/gm, '<li>$1</li>');
       text = text.replace(/(<li>.*?<\/li>\n<li>.*?<\/li>)/gs, '<ul>$1</ul>');
       
       // Important sections
       text = text.replace(/IMPORTANT:(.*?)(?=\n\n|$)/gs, '<div class="important-note"><strong>IMPORTANT:</strong>$1</div>');
       text = text.replace(/NOTE:(.*?)(?=\n\n|$)/gs, '<div class="note"><strong>NOTE:</strong>$1</div>');
       text = text.replace(/DISCLAIMER:(.*?)(?=\n\n|$)/gs, '<div class="disclaimer-box"><strong>DISCLAIMER:</strong>$1</div>');
       
       return text;
   }
});