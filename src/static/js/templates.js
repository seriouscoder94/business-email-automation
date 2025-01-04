// Template Management
const API_BASE_URL = '';

let currentTemplate = null;
let leads = [];
let templates = [];

// Load all templates
async function loadTemplates() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/templates`);
        templates = await response.json();
        
        const container = document.querySelector('#templates-section .grid');
        container.innerHTML = templates.map(template => `
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h3 class="text-lg font-bold mb-2">${template.name}</h3>
                <p class="text-gray-600 mb-4">${template.subject}</p>
                <div class="space-y-2">
                    <button onclick="previewTemplate('${template.id}')" 
                            class="w-full bg-blue-100 text-blue-700 px-4 py-2 rounded-lg hover:bg-blue-200">
                        Preview
                    </button>
                    <button onclick="viewTemplate('${template.id}')"
                            class="w-full bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200">
                        View
                    </button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading templates:', error);
    }
}

// View template details
function viewTemplate(templateId) {
    const template = templates.find(t => t.id === templateId);
    if (template) {
        alert(`Template: ${template.name}\n\nSubject: ${template.subject}\n\nContent: ${template.content}`);
    }
}

// Preview template with lead data
async function previewTemplate(templateId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/templates/${templateId}/preview`);
        const preview = await response.json();
        if (preview.success) {
            const previewModal = document.getElementById('preview-modal');
            const previewContent = document.getElementById('preview-content');
            
            previewContent.innerHTML = `
                <h3 class="text-lg font-bold mb-2">Subject:</h3>
                <p class="mb-4">${preview.subject}</p>
                <h3 class="text-lg font-bold mb-2">Content:</h3>
                <p class="whitespace-pre-line">${preview.content}</p>
            `;
            
            previewModal.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error previewing template:', error);
    }
}

// Close preview modal
function closePreviewModal() {
    const previewModal = document.getElementById('preview-modal');
    previewModal.classList.add('hidden');
}

// Load template select options
async function loadTemplateSelect() {
    try {
        const select = document.getElementById('template-select');
        select.innerHTML = templates.map(template => 
            `<option value="${template.id}">${template.name}</option>`
        ).join('');
        
        // Trigger preview of first template
        if (templates.length > 0) {
            previewTemplate(templates[0].id);
        }
    } catch (error) {
        console.error('Error loading template select:', error);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTemplates();
});

// Business email templates
const businessTemplates = {
    // Templates for businesses with NO website
    noWebsite: {
        general: {
            subject: "Ready to Boost {{business_name}} Online? 🌐",
            content: `Hi {{owner_name}},

I noticed that {{business_name}} doesn't have a website yet, and I wanted to reach out because I believe you're missing out on valuable opportunities to grow your business.

Did you know that:
• 97% of consumers search online for local businesses
• 70% of customers visit a business's website before making a purchase
• Businesses with websites are seen as 3x more credible by potential customers

Having a professional website could help {{business_name}}:
✓ Attract new customers 24/7
✓ Build credibility in your local market
✓ Showcase your products/services professionally
✓ Save time by automating common customer questions

We specialize in creating simple, effective websites that:
• Are easy to update yourself
• Look great on all devices
• Load quickly
• Connect to your social media
• Help you appear in local searches

Would you be open to a 15-minute chat about how a website could help {{business_name}} grow? I'd love to learn more about your business goals and share some examples of how other local businesses have benefited from their first website.

Book a free consultation here: [Insert link]

Best regards,
{{sender_name}}

P.S. If you book this week, I'll include a free local SEO audit to help your business get found online!`
        },
        restaurant: {
            subject: "Stop Losing 60% of Your Customers to Third-Party Apps",
            content: `Dear {{owner_name}},

Did you know that 78% of diners check restaurant websites before choosing where to eat? Without a website, {{business_name}} is missing out on these potential customers and paying high commissions to third-party delivery apps.

Current Challenges You're Facing:
• Losing 30% of revenue to delivery app commissions
• No control over your online presence
• Missing out on direct customer relationships
• Limited ability to showcase your menu and ambiance

Let's Get Your Restaurant Online:
1. Custom Restaurant Website
   • Professional food photography
   • Mobile-friendly design
   • Easy-to-update digital menu
   • Direct ordering system

2. Customer Connection Tools
   • Newsletter signup
   • Special offers page
   • Event announcements
   • Customer loyalty program

3. Direct Ordering System
   • Zero commission fees
   • Customer database ownership
   • Automated order processing
   • Real-time order tracking

4. Local SEO Setup
   • Google Business Profile
   • Local search optimization
   • Review management
   • Map integration

Quick Facts:
• Setup Time: 2-3 weeks
• Monthly Cost: Less than 2 delivery app orders
• ROI: Average 300% first year
• Support: 24/7 customer service

Would you like to see how other local restaurants increased their profits by 40% after launching their websites? I can show you examples of restaurants similar to {{business_name}} that now save $2,000+ monthly in delivery app fees.

Best regards,
{{sender_name}}

P.S. Book a free consultation this week and get 3 months of website hosting free!`
        },
        salon: {
            subject: "Elevate {{business_name}} with a Professional Beauty Website",
            content: `Dear {{owner_name}},

I noticed {{business_name}} doesn't have a website yet, and I specialize in creating stunning websites for salons and spas. A custom website would transform how clients interact with your business:

• Smart Booking System
  - 24/7 online appointment scheduling
  - Automatic confirmation emails
  - SMS reminders to reduce no-shows
  - Stylist availability calendar

• Service Showcase
  - Beautiful gallery of your work
  - Detailed service menu with pricing
  - Before/after transformations
  - Featured hair/beauty trends

• Client Experience
  - New client forms online
  - Product recommendations
  - Style inspiration gallery
  - Mobile-friendly design

• Business Growth
  - Gift card purchases
  - Product sales online
  - Review collection system
  - Social media integration

Would you like to see how a professional website could help {{business_name}} attract more clients and simplify your booking process? I'd be happy to show you examples of other salon websites we've created.

Best regards,
{{sender_name}}`
        },
        restaurant: {
            subject: "Get {{business_name}} Online and Stop Losing Business to Third-Party Apps",
            content: `Dear {{owner_name}},

I noticed {{business_name}} doesn't have its own website, which means you're probably losing customers to third-party delivery apps that charge high commissions and own your customer relationships.

Did you know:
• 70% of diners check a restaurant's menu online before deciding where to eat
• Third-party apps charge 15-30% commission on every order
• Restaurants without websites lose 40% of potential first-time customers

I help restaurants like yours establish their first online presence with:

• Simple Online Menu
  - Easy-to-read format
  - Mobile-friendly design
  - PDF download option
  - Daily specials section

• Basic Online Ordering
  - Commission-free orders
  - Phone/email notifications
  - Simple checkout process
  - Payment processing

• Essential Contact Info
  - Business hours
  - Location/directions
  - Phone numbers
  - Parking information

• Social Proof
  - Photo gallery
  - Customer reviews
  - Health ratings
  - Awards/recognition

The best part? You can have this up and running in just 2 weeks, starting at $X/month with no commission fees.

Would you like to see how other local restaurants got started with their first website? I can show you some examples of restaurants that now save over $2,000/month in delivery app commissions.

Best regards,
{{sender_name}}`
        },
        retail: {
            subject: "Transform {{business_name}} with a Modern E-commerce Website",
            content: `Dear {{owner_name}},

I noticed {{business_name}} doesn't have a website yet, and I specialize in creating powerful e-commerce platforms for retail businesses. A custom online store could revolutionize how you sell:

• Advanced E-commerce Features
  - Product catalog management
  - Inventory sync across channels
  - Multiple payment options
  - Secure checkout process

• Customer Shopping Experience
  - Smart product search
  - Size/color variants
  - Wishlist functionality
  - Recently viewed items

• Marketing Tools
  - Abandoned cart recovery
  - Customer segmentation
  - Email marketing integration
  - Social media shopping

• Business Operations
  - Order management system
  - Shipping label generation
  - Return processing
  - Sales analytics

Would you like to see how an e-commerce website could help {{business_name}} reach customers 24/7? I'd be happy to show you examples of other retail stores that have significantly increased their sales through online channels.

Best regards,
{{sender_name}}`
        },
        professional: {
            subject: "Establish {{business_name}}'s Digital Authority with a Professional Website",
            content: `Dear {{owner_name}},

I noticed {{business_name}} doesn't have a website yet, and I specialize in creating authoritative online platforms for professional service providers. A custom website could establish your digital presence and attract high-value clients:

• Professional Credibility
  - Expertise showcase
  - Case studies/success stories
  - Industry certifications
  - Team member profiles

• Client Acquisition
  - Service descriptions
  - Consultation scheduling
  - Lead capture forms
  - Client testimonials

• Digital Resources
  - Knowledge base articles
  - Downloadable resources
  - Industry insights blog
  - Newsletter subscription

• Client Portal
  - Secure document sharing
  - Project status tracking
  - Communication hub
  - Payment processing

Would you like to see how a professional website could help {{business_name}} attract more qualified leads? I'd be happy to show you examples of other professional service websites we've created that are consistently generating new business opportunities.

Best regards,
{{sender_name}}`
        },
        dental: {
            subject: "Transform {{business_name}}'s Patient Experience with a Modern Dental Website",
            content: `Dear {{owner_name}},

I noticed {{business_name}} doesn't have a website yet, and I specialize in creating patient-focused websites for dental practices. A custom website could revolutionize how you engage with patients:

• Patient Management
  - Online appointment booking
  - New patient registration
  - Insurance verification
  - Treatment history access

• Service Information
  - Treatment explanations
  - Before/after gallery
  - Technology showcase
  - Insurance/payment options

• Patient Education
  - Procedure videos
  - Care instructions
  - FAQ section
  - Oral health blog

• Practice Growth
  - Patient reviews integration
  - Special offers management
  - Referral program
  - Emergency contact system

Would you like to see how a modern website could help {{business_name}} attract new patients and improve patient satisfaction? I'd be happy to show you examples of other dental practices that have significantly grown their patient base through their website.

Best regards,
{{sender_name}}`
        },
        realestate: {
            subject: "Transform {{business_name}}'s Property Marketing with a Modern Real Estate Website",
            content: `Dear {{owner_name}},

I noticed {{business_name}} doesn't have a website yet, and I specialize in creating powerful real estate platforms. A custom website could revolutionize how you showcase properties and connect with buyers:

• Property Showcase
  - HD photo galleries
  - Virtual 360° tours
  - Video walkthroughs
  - Interactive floor plans

• Search Experience
  - Advanced property filters
  - Map-based search
  - Save favorite listings
  - Price alert notifications

• Lead Generation
  - Property inquiry forms
  - Showing scheduler
  - Market report signup
  - Newsletter subscription

• Agent Tools
  - CRM integration
  - Lead management
  - Automated follow-ups
  - Performance analytics

Would you like to see how a modern real estate website could help {{business_name}} showcase properties more effectively? I'd be happy to show you examples of other real estate websites we've created that are consistently generating qualified leads.

Best regards,
{{sender_name}}`
        },
        law: {
            subject: "Establish {{business_name}}'s Legal Authority with a Professional Law Firm Website",
            content: `Dear {{owner_name}},

I noticed {{business_name}} doesn't have a website yet, and I specialize in creating authoritative websites for law firms. A custom website could establish your firm's credibility and attract qualified clients:

• Practice Areas
  - Detailed service descriptions
  - Case study highlights
  - Success stories
  - Settlement records

• Client Resources
  - Legal guides/FAQs
  - Document templates
  - Blog/news section
  - Newsletter signup

• Client Acquisition
  - Consultation scheduler
  - Contact forms by practice area
  - Live chat integration
  - Emergency contact options

• Firm Credibility
  - Attorney profiles
  - Bar certifications
  - Media mentions
  - Client testimonials

Would you like to see how a professional website could help {{business_name}} establish authority and attract more clients? I'd be happy to show you examples of other law firm websites we've created that are effectively generating qualified leads.

Best regards,
{{sender_name}}`
        },
        construction: {
            subject: "Showcase {{business_name}}'s Projects with a Professional Construction Website",
            content: `Dear {{owner_name}},

I noticed {{business_name}} doesn't have a website yet, and I specialize in creating powerful platforms for construction companies. A custom website could transform how you showcase your work and attract new clients:

• Project Portfolio
  - HD project galleries
  - Before/after comparisons
  - Time-lapse videos
  - Project descriptions

• Service Showcase
  - Detailed service listings
  - Equipment capabilities
  - Safety certifications
  - Team expertise

• Client Resources
  - Project timeline tracker
  - Online quote requests
  - Material calculators
  - FAQ section

• Business Growth
  - Lead capture forms
  - Testimonial showcase
  - Project blog
  - Newsletter signup

Would you like to see how a professional website could help {{business_name}} showcase your expertise and attract larger projects? I'd be happy to show you examples of other construction websites we've created that are consistently generating qualified leads.

Best regards,
{{sender_name}}`
        },
        photography: {
            subject: "Showcase {{business_name}}'s Portfolio with a Stunning Photography Website",
            content: `Dear {{owner_name}},

I noticed {{business_name}} doesn't have a website yet, and I specialize in creating beautiful platforms for photographers. A custom website could transform how you showcase your work and connect with clients:

• Portfolio Showcase
  - Full-screen galleries
  - Category organization
  - Image protection
  - Custom watermarks

• Client Experience
  - Online booking system
  - Package comparison
  - Digital contracts
  - Client galleries

• Business Tools
  - Print shop integration
  - Digital delivery
  - Invoice generation
  - Session scheduling

• Marketing Features
  - Blog integration
  - SEO optimization
  - Social media feeds
  - Email marketing

Would you like to see how a professional website could help {{business_name}} showcase your work and attract more clients? I'd be happy to show you examples of other photography websites we've created that are effectively generating bookings.

Best regards,
{{sender_name}}`
        },
        petgrooming: {
            subject: "Transform {{business_name}}'s Pet Services with a Modern Website",
            content: `Dear {{owner_name}},

I noticed {{business_name}} doesn't have a website yet, and I specialize in creating powerful platforms for pet service businesses. A custom website could revolutionize how you connect with pet owners:

• Booking System
  - Online appointment scheduling
  - Service package selection
  - Pet profile management
  - Automated reminders

• Service Showcase
  - Before/after gallery
  - Service descriptions
  - Pricing packages
  - Special offers

• Pet Parent Resources
  - Care guidelines
  - Grooming tips
  - FAQ section
  - Emergency contacts

• Business Growth
  - Client reviews
  - Loyalty program
  - Gift certificates
  - Referral system

Would you like to see how a modern website could help {{business_name}} attract more pet parents? I'd be happy to show you examples of other pet service websites we've created that are consistently generating new appointments.

Best regards,
{{sender_name}}`
        },
        bakery: {
            subject: "Sweeten {{business_name}}'s Success with a Custom Bakery Website",
            content: `Dear {{owner_name}},

I noticed {{business_name}} doesn't have a website yet, and I specialize in creating delightful platforms for bakeries. A custom website could transform how you showcase your creations:

• Product Showcase
  - HD photo galleries
  - Product categories
  - Seasonal specials
  - Custom cake builder

• Online Ordering
  - Easy order system
  - Custom cake requests
  - Delivery scheduling
  - Pick-up management

• Customer Experience
  - Order tracking
  - Loyalty rewards
  - Gift cards
  - Newsletter signup

• Business Tools
  - Inventory management
  - Order analytics
  - Customer database
  - Marketing automation

Would you like to see how a modern website could help {{business_name}} increase orders and delight customers? I'd be happy to show you examples of other bakery websites we've created that are successfully generating online sales.

Best regards,
{{sender_name}}`
        }
    },
    
    // Templates for businesses that HAVE a website
    touchup: {
        general: {
            subject: "I Have Some Ideas to Enhance {{business_name}}'s Website 🚀",
            content: `Hi {{owner_name}},

I just visited {{business_name}}'s website and was impressed by what you've built. I particularly liked [specific feature] and how you've [positive observation].

As someone who specializes in website optimization, I noticed a few opportunities to enhance your site's performance and user experience:

Current Website Strengths:
✓ [Specific positive feature]
✓ [Another positive aspect]
✓ [Third positive point]

Potential Enhancements:
1. User Experience
   • Streamline the customer journey
   • Optimize for mobile devices
   • Improve page load speed

2. Modern Features
   • Smart booking/payment systems
   • Customer account portal
   • Automated email notifications

3. Business Growth
   • SEO optimization
   • Analytics dashboard
   • Marketing integrations

Would you be interested in a free website audit? I'll analyze:
• Mobile responsiveness
• Page load speeds
• SEO performance
• Conversion optimization
• Security status

I've helped other local businesses achieve:
• 40% faster load times
• 55% more mobile conversions
• 70% increase in online inquiries

Let's schedule a 15-minute call to review your goals and explore how these improvements could benefit {{business_name}}.

Book your free website audit here: [Insert link]

Best regards,
{{sender_name}}

P.S. The audit is completely free, and you'll receive a detailed report regardless of whether we work together.`
        },
        restaurant: {
            subject: "Your Website Analysis: {{business_name}}'s ${{potential_revenue}} Monthly Opportunity",
            content: `Dear {{owner_name}},

I've completed a detailed technical analysis of {{business_name}}'s website, comparing it against top-performing restaurant sites. Here's what I found:

Current Website Performance Metrics:
✗ Mobile Load Time: 6.2s (Industry Standard: 2.5s)
✗ Mobile Conversion Rate: 1.2% (Industry Leader: 4.8%)
✗ Cart Abandonment: 82% (Industry Average: 67%)
✗ Online Order Value: $32 (Industry Average: $48)

Technical Issues Impacting Revenue:
1. Speed & Performance
   • Images not optimized (causing 3.4s delay)
   • No content delivery network
   • Missing browser caching
   • Slow server response time

2. Mobile Experience
   • Non-responsive design elements
   • Touch targets too small
   • Font size issues on mobile
   • Horizontal scrolling problems

3. Ordering System
   • 6-step checkout (should be 3)
   • No saved customer preferences
   • Limited payment options
   • Manual order processing

4. Menu Engineering
   • Static PDF menu only
   • No dish photos
   • No dietary filters
   • No upsell suggestions

Proposed Technical Solutions:
1. Performance Optimization
   • Image optimization pipeline
   • CloudFront CDN implementation
   • Browser caching setup
   • Server upgrade

2. Mobile Enhancement
   • Progressive Web App conversion
   • Touch-friendly interface
   • Responsive design fixes
   • Mobile-first checkout

3. Order Flow Redesign
   • 3-step smart checkout
   • Customer profiles
   • Multiple payment gateways
   • Kitchen display integration

4. Dynamic Menu System
   • Interactive menu builder
   • Photo integration
   • Smart filtering system
   • AI-powered recommendations

Expected Impact (Based on Current Traffic):
• Load Time: 6.2s → 1.8s
• Mobile Conversion: 1.2% → 4.5%
• Cart Abandonment: 82% → 64%
• Avg Order Value: $32 → $45

Projected Monthly Impact:
• Additional Orders: +{{additional_orders}}
• Revenue Increase: ${{revenue_increase}}
• Labor Hours Saved: {{labor_hours}}
• Customer Retention: +{{retention_increase}}%

I've helped 12 restaurants in {{business_location}} achieve similar results. Would you like to see their before/after metrics?

Best regards,
{{sender_name}}

P.S. I have a technical presentation ready showing exactly how we'll implement these changes. When would be a good time to review it?`
        },
        retail: {
            subject: "Upgrade {{business_name}}'s E-commerce Experience",
            content: `Dear {{owner_name}},

I just visited {{business_name}}'s online store and noticed several opportunities to enhance your current e-commerce setup. While you have a good foundation, here are some modern features we could add to help you compete with major retailers:

Current Website Pain Points:
• High cart abandonment rate
• Limited product discovery
• Basic mobile shopping experience
• Manual inventory management

Proposed Website Upgrades:
• Advanced Shopping Experience
  - AI-powered product recommendations
  - Virtual try-on technology
  - Size prediction system
  - Quick-view product cards

• Checkout Optimization
  - One-click purchase
  - Multiple payment options
  - Address verification
  - Smart shipping calculator

• Mobile Commerce 2.0
  - Progressive web app
  - Image search
  - Voice shopping
  - Mobile wallet integration

• Operations Enhancement
  - Real-time inventory sync
  - Automated reordering
  - Multi-channel management
  - Advanced analytics

Looking at your current setup, these improvements could significantly impact your sales. Other retailers we've helped upgrade saw:
• 55% reduction in cart abandonment
• 70% increase in mobile sales
• 40% higher average order value
• 30% increase in repeat customers

Would you like to discuss how we could implement these upgrades to help {{business_name}} compete with major online retailers? I can show you specific examples of how these features have transformed other e-commerce websites.

Best regards,
{{sender_name}}`
        },
        dental: {
            subject: "Modernize {{business_name}}'s Patient Experience Online",
            content: `Dear {{owner_name}},

After reviewing {{business_name}}'s website, I've identified several opportunities to enhance your patient experience:

Current Website Limitations:
• Basic appointment booking
• Manual form submission
• Limited patient portal
• Outdated resource section

Recommended Upgrades:
• Smart Scheduling
  - Insurance verification
  - Appointment reminders
  - Emergency requests
  - Family scheduling

• Patient Portal
  - Treatment history
  - Payment processing
  - Document access
  - Secure messaging

• Educational Resources
  - Procedure videos
  - Care instructions
  - Interactive guides
  - FAQ automation

• Practice Growth
  - Review management
  - Referral tracking
  - Treatment plans
  - Follow-up automation

I noticed several leading dental practices have implemented similar features with great success. Would you like to discuss how these improvements could help {{business_name}} improve patient satisfaction? Our dental clients typically see a 40% increase in new patient appointments after these updates.

Best regards,
{{sender_name}}`
        },
        realestate: {
            subject: "Enhance {{business_name}}'s Property Website Performance",
            content: `Dear {{owner_name}},

After reviewing {{business_name}}'s website, I've identified several opportunities to enhance your property listings and lead generation:

Current Website Limitations:
• Basic property search
• Limited virtual tours
• Manual showing requests
• Basic lead capture

Recommended Upgrades:
• Advanced Property Search
  - Map integration
  - Save searches
  - Price alerts
  - Similar listings

• Virtual Experience
  - 3D walkthroughs
  - Video tours
  - Drone footage
  - AR viewing

• Lead Generation
  - Smart forms
  - Chat integration
  - Automated follow-up
  - Lead scoring

• Agent Tools
  - Showing scheduler
  - Document signing
  - Client portal
  - Market reports

I noticed several leading real estate firms have implemented similar features with great success. Would you like to discuss how these improvements could help {{business_name}} generate more qualified leads? Our real estate clients typically see an 85% increase in showing requests after these updates.

Best regards,
{{sender_name}}`
        },
        law: {
            subject: "Modernize {{business_name}}'s Legal Website for Better Client Acquisition",
            content: `Dear {{owner_name}},

After reviewing {{business_name}}'s website, I've identified several opportunities to enhance your online presence and client acquisition:

Current Website Limitations:
• Basic practice area pages
• Manual intake process
• Limited client resources
• Outdated case results

Recommended Upgrades:
• Practice Area Enhancement
  - Interactive guides
  - Video explanations
  - Case result database
  - Client testimonials

• Client Intake
  - Smart intake forms
  - Document upload
  - Case evaluation
  - Secure messaging

• Resource Center
  - Legal guides
  - Video library
  - Blog platform
  - Newsletter system

• Credibility Features
  - Attorney profiles
  - Awards section
  - Media mentions
  - Client reviews

I noticed several leading law firms have implemented similar features with great success. Would you like to discuss how these improvements could help {{business_name}} attract more qualified clients? Our law firm clients typically see a 65% increase in qualified leads after these updates.

Best regards,
{{sender_name}}`
        },
        construction: {
            subject: "Enhance {{business_name}}'s Project Showcase Website",
            content: `Dear {{owner_name}},

After reviewing {{business_name}}'s website, I've identified several opportunities to enhance your project presentation and lead generation:

Current Website Limitations:
• Basic project gallery
• Limited project details
• Manual quote system
• Outdated portfolio

Recommended Upgrades:
• Project Showcase
  - 360° project views
  - Before/after sliders
  - Time-lapse videos
  - Project filters

• Estimation Tools
  - Online calculator
  - Material selector
  - Timeline estimator
  - Budget planner

• Client Portal
  - Project tracking
  - Document sharing
  - Progress photos
  - Communication hub

• Credibility Features
  - Safety records
  - Certifications
  - Team profiles
  - Client reviews

I noticed several leading construction companies have implemented similar features with great success. Would you like to discuss how these improvements could help {{business_name}} win more projects? Our construction clients typically see a 70% increase in qualified leads after these updates.

Best regards,
{{sender_name}}`
        },
        photography: {
            subject: "Modernize {{business_name}}'s Photography Portfolio Website",
            content: `Dear {{owner_name}},

After reviewing {{business_name}}'s website, I've identified several opportunities to enhance your portfolio and booking system:

Current Website Limitations:
• Slow gallery loading
• Basic booking system
• Limited client access
• Manual delivery process

Recommended Upgrades:
• Portfolio Enhancement
  - Fast-loading galleries
  - Category filtering
  - Lightbox viewing
  - Mobile optimization

• Booking System
  - Package selection
  - Availability calendar
  - Contract signing
  - Payment processing

• Client Galleries
  - Private access
  - Download options
  - Sharing features
  - Print ordering

• Business Tools
  - Lead tracking
  - Email marketing
  - Social integration
  - Analytics dashboard

I noticed several successful photographers have implemented similar features with great results. Would you like to discuss how these improvements could help {{business_name}} book more clients? Our photography clients typically see a 75% increase in bookings after these updates.

Best regards,
{{sender_name}}`
        },
        petgrooming: {
            subject: "Upgrade {{business_name}}'s Pet Service Website",
            content: `Dear {{owner_name}},

After reviewing {{business_name}}'s website, I've identified several opportunities to enhance your booking system and client experience:

Current Website Limitations:
• Basic appointment system
• Manual reminders
• Limited service info
• Basic pet profiles

Recommended Upgrades:
• Smart Booking
  - Real-time availability
  - Service packages
  - Multi-pet booking
  - Mobile scheduling

• Client Management
  - Pet profiles
  - Service history
  - Photo sharing
  - Care notes

• Service Information
  - Service videos
  - Price calculator
  - Package comparisons
  - FAQ system

• Marketing Tools
  - Review management
  - Loyalty program
  - Referral system
  - Email marketing

I noticed several leading pet groomers have implemented similar features with great success. Would you like to discuss how these improvements could help {{business_name}} increase bookings? Our pet service clients typically see a 60% increase in online appointments after these updates.

Best regards,
{{sender_name}}`
        },
        bakery: {
            subject: "Enhance {{business_name}}'s Bakery Website for More Orders",
            content: `Dear {{owner_name}},

After reviewing {{business_name}}'s website, I've identified several opportunities to enhance your online ordering and customer experience:

Current Website Limitations:
• Basic product display
• Manual order process
• Limited customization
• Basic inventory management

Recommended Upgrades:
• Product Showcase
  - HD photo galleries
  - 360° cake views
  - Flavor profiles
  - Seasonal collections

• Order System
  - Custom cake designer
  - Order scheduling
  - Delivery tracking
  - Quote calculator

• Customer Features
  - Favorites list
  - Order history
  - Event reminders
  - Gift cards

• Business Tools
  - Inventory sync
  - Order analytics
  - Customer database
  - Marketing automation

I noticed several successful bakeries have implemented similar features with great results. Would you like to discuss how these improvements could help {{business_name}} increase orders? Our bakery clients typically see an 85% increase in online orders after these updates.

Best regards,
{{sender_name}}`
        }
    }
}
