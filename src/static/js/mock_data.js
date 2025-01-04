// Mock data for testing when API is unavailable
const MOCK_DATA = {
    businesses: [
        {
            name: "The Test Restaurant",
            address: "123 Demo Street, Test City",
            business_type: "restaurant",
            phone: "(555) 555-1234",
            website: "http://testrestaurant.com",
            email: "contact@testrestaurant.com",
            rating: 4.5,
            has_website: true,
            source: "mock",
            discovery_date: new Date().toISOString()
        },
        {
            name: "Mock Cafe",
            address: "456 Sample Ave, Test City",
            business_type: "restaurant",
            phone: "(555) 555-5678",
            website: "",
            email: "",
            rating: 4.0,
            has_website: false,
            source: "mock",
            discovery_date: new Date().toISOString()
        },
        {
            name: "Test Retail Store",
            address: "789 Example Blvd, Test City",
            business_type: "retail",
            phone: "(555) 555-9012",
            website: "http://testretail.com",
            email: "info@testretail.com",
            rating: 3.5,
            has_website: true,
            source: "mock",
            discovery_date: new Date().toISOString()
        }
    ],
    
    generateMockBusinesses: function(location, businessType, count = 5) {
        const streetNames = ['Main', 'Oak', 'Maple', 'Cedar', 'Pine', 'Elm', 'Washington', 'Market'];
        const businessTypes = {
            restaurant: ['Cafe', 'Bistro', 'Restaurant', 'Diner', 'Grill', 'Eatery'],
            retail: ['Shop', 'Store', 'Boutique', 'Market', 'Outlet', 'Emporium'],
            healthcare: ['Clinic', 'Medical Center', 'Healthcare', 'Wellness Center', 'Medical Office'],
            technology: ['Tech Solutions', 'IT Services', 'Digital', 'Tech Hub', 'Computing'],
            professional: ['Services', 'Consulting', 'Associates', 'Group', 'Partners']
        };
        
        const suffixes = businessTypes[businessType] || businessTypes.professional;
        const businesses = [];
        
        for (let i = 0; i < count; i++) {
            const hasWebsite = Math.random() > 0.3;
            const name = `Test ${suffixes[Math.floor(Math.random() * suffixes.length)]} ${i + 1}`;
            const street = streetNames[Math.floor(Math.random() * streetNames.length)];
            
            businesses.push({
                name: name,
                address: `${Math.floor(Math.random() * 999) + 1} ${street} St, ${location}`,
                business_type: businessType,
                phone: `(555) ${String(Math.floor(Math.random() * 900) + 100).padStart(3, '0')}-${String(Math.floor(Math.random() * 9000) + 1000)}`,
                website: hasWebsite ? `http://www.${name.toLowerCase().replace(/\s+/g, '')}.com` : '',
                email: hasWebsite ? `contact@${name.toLowerCase().replace(/\s+/g, '')}.com` : '',
                rating: Math.floor(Math.random() * 30 + 20) / 10,
                has_website: hasWebsite,
                source: 'mock',
                discovery_date: new Date().toISOString()
            });
        }
        
        return businesses;
    },
    
    mockApiResponse: function(location, businessType) {
        return {
            success: true,
            businesses: this.generateMockBusinesses(location, businessType),
            total: 5,
            source: 'mock'
        };
    },
    
    mockWebsiteCheck: function(businesses) {
        return {
            success: true,
            results: businesses.map(business => ({
                ...business,
                website_status: business.has_website ? 'active' : 'not_found',
                last_checked: new Date().toISOString()
            }))
        };
    },
    
    mockEnrichment: function(businesses) {
        return {
            success: true,
            results: businesses.map(business => ({
                ...business,
                enriched_data: {
                    employees: Math.floor(Math.random() * 50) + 1,
                    year_founded: 2000 + Math.floor(Math.random() * 23),
                    revenue_range: '$1M - $5M',
                    social_media: {
                        facebook: business.has_website ? `https://facebook.com/${business.name.toLowerCase().replace(/\s+/g, '')}` : '',
                        linkedin: business.has_website ? `https://linkedin.com/company/${business.name.toLowerCase().replace(/\s+/g, '')}` : ''
                    }
                },
                enrichment_date: new Date().toISOString()
            }))
        };
    },
    
    mockExport: function(businesses, format) {
        return {
            success: true,
            download_url: '#',
            message: `Mock export of ${businesses.length} businesses completed`,
            format: format,
            timestamp: new Date().toISOString()
        };
    }
};
