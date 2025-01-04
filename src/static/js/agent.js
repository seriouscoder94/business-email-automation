// AI Agent Sam - Frontend JavaScript

class AIAgentUI {
    constructor() {
        this.initializeElements();
        this.attachEventListeners();
        this.currentStep = 1;
        this.businesses = [];
    }

    initializeElements() {
        // Buttons
        this.searchBtn = document.getElementById('searchBtn');
        this.checkWebsiteBtn = document.getElementById('checkWebsiteBtn');
        this.enrichDataBtn = document.getElementById('enrichDataBtn');
        this.exportBtn = document.getElementById('exportBtn');

        // Input fields
        this.regionSelect = document.getElementById('region');
        this.industrySelect = document.getElementById('industry');
        this.keywordsInput = document.getElementById('keywords');

        // Filters
        this.regionFilter = document.getElementById('regionFilter');
        this.industryFilter = document.getElementById('industryFilter');
        this.websiteFilter = document.getElementById('websiteFilter');

        // Results
        this.resultsBody = document.getElementById('resultsBody');
        this.toast = document.getElementById('toast');
    }

    attachEventListeners() {
        this.searchBtn.addEventListener('click', () => this.startSearch());
        this.checkWebsiteBtn.addEventListener('click', () => this.checkWebsites());
        this.enrichDataBtn.addEventListener('click', () => this.enrichData());
        this.exportBtn.addEventListener('click', () => this.exportLeads());

        // Filter listeners
        this.regionFilter.addEventListener('change', () => this.applyFilters());
        this.industryFilter.addEventListener('change', () => this.applyFilters());
        this.websiteFilter.addEventListener('change', () => this.applyFilters());
    }

    async startSearch() {
        try {
            this.setLoading(this.searchBtn, true);
            this.updateProgress(1);

            const searchParams = {
                region: this.regionSelect.value,
                industry: this.industrySelect.value,
                keywords: this.keywordsInput.value.split(',').map(k => k.trim())
            };

            const response = await fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(searchParams)
            });

            if (!response.ok) throw new Error('Search failed');

            this.businesses = await response.json();
            this.updateResults();
            this.showToast('Search completed successfully!', 'success');
            this.updateProgress(2);

        } catch (error) {
            this.showToast('Error during search: ' + error.message, 'error');
        } finally {
            this.setLoading(this.searchBtn, false);
        }
    }

    async checkWebsites() {
        try {
            this.setLoading(this.checkWebsiteBtn, true);
            this.updateProgress(2);

            const response = await fetch('/api/check-websites', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ businesses: this.businesses })
            });

            if (!response.ok) throw new Error('Website check failed');

            this.businesses = await response.json();
            this.updateResults();
            this.showToast('Website check completed!', 'success');
            this.updateProgress(3);

        } catch (error) {
            this.showToast('Error checking websites: ' + error.message, 'error');
        } finally {
            this.setLoading(this.checkWebsiteBtn, false);
        }
    }

    async enrichData() {
        try {
            this.setLoading(this.enrichDataBtn, true);
            this.updateProgress(3);

            const response = await fetch('/api/enrich-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ businesses: this.businesses })
            });

            if (!response.ok) throw new Error('Data enrichment failed');

            this.businesses = await response.json();
            this.updateResults();
            this.showToast('Data enrichment completed!', 'success');
            this.updateProgress(4);

        } catch (error) {
            this.showToast('Error enriching data: ' + error.message, 'error');
        } finally {
            this.setLoading(this.enrichDataBtn, false);
        }
    }

    async exportLeads() {
        try {
            this.setLoading(this.exportBtn, true);

            const response = await fetch('/api/export-leads', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ businesses: this.businesses })
            });

            if (!response.ok) throw new Error('Export failed');

            const result = await response.json();
            this.showToast(`Exported ${result.count} leads successfully!`, 'success');

        } catch (error) {
            this.showToast('Error exporting leads: ' + error.message, 'error');
        } finally {
            this.setLoading(this.exportBtn, false);
        }
    }

    updateResults() {
        this.resultsBody.innerHTML = '';
        
        const filteredBusinesses = this.getFilteredBusinesses();
        
        filteredBusinesses.forEach(business => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${business.name}</td>
                <td>${business.industry}</td>
                <td>${business.region}</td>
                <td>
                    ${business.email ? `<div>📧 ${business.email}</div>` : ''}
                    ${business.phone ? `<div>📞 ${business.phone}</div>` : ''}
                </td>
                <td>
                    <span class="badge ${business.has_website ? 'badge-success' : 'badge-warning'}">
                        ${business.has_website ? 'Has Website' : 'No Website'}
                    </span>
                </td>
                <td>
                    <button onclick="aiAgent.editBusiness('${business.id}')" class="button">Edit</button>
                    <button onclick="aiAgent.deleteBusiness('${business.id}')" class="button">Delete</button>
                </td>
            `;
            this.resultsBody.appendChild(row);
        });

        // Update filter options
        this.updateFilterOptions();
    }

    getFilteredBusinesses() {
        return this.businesses.filter(business => {
            const regionMatch = !this.regionFilter.value || business.region === this.regionFilter.value;
            const industryMatch = !this.industryFilter.value || business.industry === this.industryFilter.value;
            const websiteMatch = !this.websiteFilter.value || 
                (this.websiteFilter.value === 'no' && !business.has_website) ||
                (this.websiteFilter.value === 'yes' && business.has_website);
            
            return regionMatch && industryMatch && websiteMatch;
        });
    }

    updateFilterOptions() {
        // Get unique values for filters
        const regions = [...new Set(this.businesses.map(b => b.region))];
        const industries = [...new Set(this.businesses.map(b => b.industry))];

        // Update region filter
        this.updateSelectOptions(this.regionFilter, regions);
        this.updateSelectOptions(this.industryFilter, industries);
    }

    updateSelectOptions(select, options) {
        const currentValue = select.value;
        select.innerHTML = '<option value="">All</option>';
        options.forEach(option => {
            const opt = document.createElement('option');
            opt.value = option;
            opt.textContent = option;
            select.appendChild(opt);
        });
        select.value = currentValue;
    }

    updateProgress(step) {
        this.currentStep = step;
        document.querySelectorAll('.progress-step').forEach(el => {
            const stepNum = parseInt(el.dataset.step);
            el.classList.remove('step-active', 'step-completed');
            if (stepNum === this.currentStep) {
                el.classList.add('step-active');
            } else if (stepNum < this.currentStep) {
                el.classList.add('step-completed');
            }
        });
    }

    setLoading(button, isLoading) {
        button.disabled = isLoading;
        button.classList.toggle('loading', isLoading);
    }

    showToast(message, type = 'success') {
        this.toast.className = `toast toast-${type} show`;
        this.toast.querySelector('.toast-message').textContent = message;
        
        setTimeout(() => {
            this.toast.classList.remove('show');
        }, 3000);
    }

    editBusiness(businessId) {
        // Implement edit functionality
        console.log('Edit business:', businessId);
    }

    deleteBusiness(businessId) {
        // Implement delete functionality
        console.log('Delete business:', businessId);
    }
}

// Initialize the UI
const aiAgent = new AIAgentUI();
