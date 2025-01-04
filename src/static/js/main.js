// Main Application Module
const App = {
    modules: {
        UI: null,
        Templates: null,
        EmailTemplates: null,
        Agent: null,
        Chat: null,
        API: null
    },

    async init() {
        console.log('Initializing application...');
        
        try {
            // Initialize core modules first
            this.modules.API = window.API;
            this.modules.UI = window.UI;
            
            // Initialize feature modules
            if (window.Templates) this.modules.Templates = window.Templates;
            if (window.EmailTemplates) this.modules.EmailTemplates = window.EmailTemplates;
            if (window.Agent) this.modules.Agent = window.Agent;
            if (window.Chat) this.modules.Chat = window.Chat;
            
            // Wait for DOM to be ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.setup());
            } else {
                await this.setup();
            }
            
            console.log('Application initialized successfully');
        } catch (error) {
            console.error('Failed to initialize application:', error);
        }
    },

    async setup() {
        console.log('Setting up application...');
        
        // Initialize UI first
        if (this.modules.UI) {
            console.log('Initializing UI...');
            await this.modules.UI.init();
        } else {
            console.error('UI module not found');
        }
        
        // Initialize other modules
        for (const [name, module] of Object.entries(this.modules)) {
            if (name !== 'UI' && module && typeof module.init === 'function') {
                console.log(`Initializing ${name}...`);
                await module.init();
            }
        }
    }
};

// Initialize application
App.init();

// Tab switching functionality
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all tabs
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });

        // Add active class to clicked tab
        button.classList.add('active');
        document.getElementById(`${button.dataset.tab}-tab`).classList.add('active');
    });
});

// File upload handling
document.getElementById('lead-upload').addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/leads/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Upload failed');
        }

        const result = await response.json();
        showNotification('Leads uploaded successfully!', 'success');
        loadLeads(); // Refresh leads table
    } catch (error) {
        showNotification('Failed to upload leads: ' + error.message, 'error');
    }
});

// Load leads into table
async function loadLeads() {
    try {
        const response = await fetch('/api/leads');
        const leads = await response.json();
        
        const tableBody = document.getElementById('leads-table-body');
        tableBody.innerHTML = '';
        
        leads.forEach(lead => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap">${lead.business_name}</td>
                <td class="px-6 py-4 whitespace-nowrap">${lead.email}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-${lead.status === 'active' ? 'green' : 'gray'}-100 text-${lead.status === 'active' ? 'green' : 'gray'}-800">
                        ${lead.status}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button class="text-indigo-600 hover:text-indigo-900 mr-4" onclick="editLead('${lead.id}')">Edit</button>
                    <button class="text-red-600 hover:text-red-900" onclick="deleteLead('${lead.id}')">Delete</button>
                </td>
            `;
            tableBody.appendChild(row);
        });

        // Update dashboard stats
        document.getElementById('totalLeads').textContent = leads.length;
    } catch (error) {
        showNotification('Failed to load leads: ' + error.message, 'error');
    }
}

// Template management
document.getElementById('new-template-btn').addEventListener('click', () => {
    // Show template creation modal
    showTemplateModal();
});

function showTemplateModal(template = null) {
    // Create and show modal for template creation/editing
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center';
    modal.innerHTML = `
        <div class="bg-white rounded-lg p-8 max-w-2xl w-full">
            <h3 class="text-lg font-medium mb-4">${template ? 'Edit' : 'New'} Template</h3>
            <form id="template-form">
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Template Name</label>
                        <input type="text" name="name" class="mt-1 block w-full border rounded-md shadow-sm p-2" 
                               value="${template ? template.name : ''}">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Subject Line</label>
                        <input type="text" name="subject" class="mt-1 block w-full border rounded-md shadow-sm p-2"
                               value="${template ? template.subject : ''}">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Email Content</label>
                        <textarea name="content" rows="10" class="mt-1 block w-full border rounded-md shadow-sm p-2">${template ? template.content : ''}</textarea>
                    </div>
                </div>
                <div class="mt-6 flex justify-end space-x-4">
                    <button type="button" class="px-4 py-2 border rounded-md" onclick="closeModal(this)">Cancel</button>
                    <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-md">Save</button>
                </div>
            </form>
        </div>
    `;
    document.body.appendChild(modal);
}

// Settings form handling
document.getElementById('settings-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const settings = {
        sendgridApiKey: document.getElementById('sendgrid-api-key').value,
        senderEmail: document.getElementById('sender-email').value,
        dailyLimit: document.getElementById('daily-limit').value
    };

    try {
        const response = await fetch('/api/settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(settings)
        });

        if (!response.ok) {
            throw new Error('Failed to save settings');
        }

        showNotification('Settings saved successfully!', 'success');
    } catch (error) {
        showNotification('Failed to save settings: ' + error.message, 'error');
    }
});

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification fixed top-4 right-4 p-4 rounded-md ${type === 'error' ? 'bg-red-500' : 'bg-green-500'} text-white`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function closeModal(element) {
    element.closest('.fixed').remove();
}

// Initial load
loadLeads();
