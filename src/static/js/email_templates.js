// Email Templates Object
const emailTemplates = {
    // NO WEBSITE TEMPLATES
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
        }
    },

    // WEBSITE TOUCHUP TEMPLATES
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
        }
    },

    // New Website Templates
    newWebsite: {
        restaurant: {
            title: 'Restaurant Website Template',
            subject: 'Transform {business_name} with a Modern Restaurant Website',
            content: `Dear {owner_name},

I noticed {business_name} could benefit from a modern website to showcase your menu and accept online orders. Here's what we can build for you:

Key Features:
• Online Menu with Photos
• Online Ordering System
• Table Reservations
• Mobile-Friendly Design
• Customer Reviews Section

Benefits:
✓ 24/7 Order Taking
✓ Reduced Phone Orders
✓ Higher Average Orders
✓ Better Customer Experience

Would you like to see some examples of restaurant websites we've built?

Best regards,
{sender_name}`
        },
        salon: {
            title: 'Salon Website Template',
            subject: 'Boost {business_name}\'s Bookings with a Professional Website',
            content: `Dear {owner_name},

I noticed {business_name} could benefit from a modern website to showcase your services and accept online bookings. Here's what we can create for you:

Key Features:
• Online Booking System
• Service Menu with Prices
• Staff Profiles
• Before/After Gallery
• Client Reviews

Benefits:
✓ 24/7 Appointment Booking
✓ Reduced Phone Time
✓ Automated Reminders
✓ More Client Reviews

Would you like to see examples of salon websites we've created?

Best regards,
{sender_name}`
        }
    },

    // Website Enhancement Templates
    enhancement: {
        'modern-features': {
            title: 'Modern Features Enhancement',
            subject: 'Enhance {business_name}\'s Website with Modern Features',
            content: `Dear {owner_name},

I visited {business_name}'s website and was impressed by what you've built. I noticed some opportunities to enhance your online presence with modern features:

Recommended Enhancements:
• Online Booking System
  - Let customers book 24/7
  - Reduce phone calls
  - Automated reminders

• Customer Portal
  - Secure client accounts
  - Order/booking history
  - Saved preferences

• Payment Integration
  - Accept online payments
  - Multiple payment methods
  - Automated invoicing

These features typically help businesses:
✓ Save 10+ hours/week
✓ Increase bookings by 40%
✓ Improve customer satisfaction

Would you like to see these features in action?

Best regards,
{sender_name}`
        },
        'performance': {
            title: 'Website Performance Optimization',
            subject: 'Speed Up {business_name}\'s Website for Better Results',
            content: `Dear {owner_name},

I analyzed {business_name}'s website and noticed some opportunities to improve its performance. Did you know:

• 53% of visitors leave if a site takes over 3 seconds to load
• Mobile users are now 60% of web traffic
• Google uses site speed as a ranking factor

Our optimization service includes:
1. Speed Optimization
   • Image compression
   • Code minification
   • Caching setup
   • CDN integration

2. Mobile Enhancement
   • Responsive design
   • Touch-friendly navigation
   • Mobile-first features

Would you like a free performance report?

Best regards,
{sender_name}`
        },
        'seo': {
            title: 'SEO Enhancement Strategy',
            subject: 'Boost {business_name}\'s Online Visibility',
            content: `Dear {owner_name},

I analyzed {business_name}'s online presence and found opportunities to improve your search visibility:

Current Opportunities:
• Local SEO optimization
• Content strategy
• Technical SEO
• Competitor analysis

Our SEO package includes:
1. Technical Optimization
   • Site structure
   • Speed optimization
   • Mobile-first indexing
   • Schema markup

2. Content Strategy
   • Keyword research
   • Content optimization
   • Local SEO
   • Regular updates

Would you like a free SEO audit report?

Best regards,
{sender_name}`
        }
    }
};

// Function to get template based on website status and business type
function getEmailTemplate(websiteStatus, businessType = 'general') {
    const templateCategory = websiteStatus ? 'touchup' : 'noWebsite';
    const templates = emailTemplates[templateCategory];
    return templates[businessType] || templates.general;
}

// Function to get template by type
function getTemplateByType(type) {
    const templates = emailTemplates.enhancement;
    return templates[type] || templates['modern-features'];
}

// Function to fill template with actual data
function fillTemplate(template, data) {
    let filledSubject = template.subject;
    let filledContent = template.content;

    // Replace all placeholders with actual data
    Object.keys(data).forEach(key => {
        const placeholder = new RegExp(`{{${key}}}`, 'g');
        filledSubject = filledSubject.replace(placeholder, data[key]);
        filledContent = filledContent.replace(placeholder, data[key]);
    });

    return {
        subject: filledSubject,
        content: filledContent
    };
}
