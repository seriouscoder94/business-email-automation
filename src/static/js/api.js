// API handling functions
const API_BASE_URL = 'http://localhost:5008/api';

async function fetchWithTimeout(url, options = {}, timeout = 30000) {  // Increased timeout to 30 seconds
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
    
    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal
        });
        clearTimeout(id);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        return response;
    } catch (error) {
        clearTimeout(id);
        if (error.name === 'AbortError') {
            throw new Error('Request timed out. Please try again.');
        }
        throw error;
    }
}

async function loadTemplates() {
    try {
        const response = await fetchWithTimeout(`${API_BASE_URL}/templates`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const templates = await response.json();
        return templates;
    } catch (error) {
        console.error('Error loading templates:', error);
        throw error;
    }
}

async function searchBusinesses(location, businessType, radius = 50) {
    try {
        console.log(`Searching businesses in ${location} of type ${businessType}`);
        const encodedLocation = encodeURIComponent(location);
        const encodedType = encodeURIComponent(businessType);
        
        const response = await fetchWithTimeout(
            `${API_BASE_URL}/search-businesses?type=${encodedType}&location=${encodedLocation}&radius=${radius}`,
            {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                }
            }
        );
        
        const data = await response.json();
        console.log('Search results:', data);
        return data;
    } catch (error) {
        console.error('Error searching businesses:', error);
        throw error;
    }
}

async function sendEmail(emailData) {
    try {
        const response = await fetchWithTimeout(`${API_BASE_URL}/send-email`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(emailData)
        });
        
        return await response.json();
    } catch (error) {
        console.error('Error sending email:', error);
        throw error;
    }
}

// Export functions
window.api = {
    loadTemplates,
    fetchWithTimeout
};

window.searchBusinesses = searchBusinesses;
window.sendEmail = sendEmail;
