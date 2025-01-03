// Business email templates
const templates = {
    restaurant: {
        subject: "Boost {{business_name}}'s Online Presence with a Custom Website",
        content: `Hello,

I noticed {{business_name}} doesn't have a website, and as someone who helps restaurants increase their online visibility, I wanted to reach out.

A website could help your restaurant:
• Showcase your menu and daily specials
• Accept online orders and reservations
• Share photos of your dishes and atmosphere
• Appear in local food searches

I'd love to create a free mock-up showing how your restaurant's website could look. No obligation - just a chance to see the possibilities.

Would you be interested in a quick 15-minute Zoom call to discuss how we could help {{business_name}} attract more customers online?

Best regards,
{{sender_name}}
{{company_name}}`
    },
    retail: {
        subject: "Expand {{business_name}}'s Reach with E-Commerce",
        content: `Hello,

I noticed {{business_name}} doesn't have an online store, and I specialize in helping retail businesses expand their reach through e-commerce.

A website with an online store could help you:
• Sell products 24/7
• Reach customers beyond your local area
• Showcase your entire inventory
• Build customer loyalty with email marketing

I'd be happy to create a free mock-up showing how your online store could look. No obligation - just a chance to see the potential.

Would you like to schedule a quick 15-minute Zoom call to discuss how we could help {{business_name}} sell online?

Best regards,
{{sender_name}}
{{company_name}}`
    },
    salon: {
        subject: "Online Booking Solution for {{business_name}}",
        content: `Hello,

I noticed {{business_name}} doesn't have online booking, and I specialize in creating websites for salons and beauty businesses.

A custom website could help you:
• Accept 24/7 online appointments
• Reduce no-shows with automatic reminders
• Showcase your services and pricing
• Share photos of your work
• Build your online presence

I'd love to create a free mock-up showing how your salon's website could look. No obligation - just a chance to see the possibilities.

Would you like to schedule a quick 15-minute Zoom call to discuss how we could help {{business_name}} streamline bookings?

Best regards,
{{sender_name}}
{{company_name}}`
    },
    gym: {
        subject: "Digital Presence for {{business_name}} - Member Portal & Online Classes",
        content: `Hello,

I noticed {{business_name}} doesn't have a website, and I specialize in creating digital solutions for fitness businesses.

A custom website could help you:
• Enable online class bookings
• Offer virtual training sessions
• Share workout schedules and updates
• Process membership sign-ups
• Track member progress

I'd be happy to create a free mock-up showing how your fitness center's website could look. No obligation - just a chance to see the potential.

Would you like to schedule a quick 15-minute Zoom call to discuss how we could help {{business_name}} grow digitally?

Best regards,
{{sender_name}}
{{company_name}}`
    },
    automotive: {
        subject: "Online Booking System for {{business_name}}",
        content: `Hello,

I noticed {{business_name}} doesn't have online scheduling, and I specialize in creating websites for automotive businesses.

A custom website could help you:
• Accept online service appointments
• Showcase your services and pricing
• Share customer reviews and testimonials
• Appear in local automotive searches
• Send automatic service reminders

I'd love to create a free mock-up showing how your automotive service website could look. No obligation - just a chance to see the possibilities.

Would you like to schedule a quick 15-minute Zoom call to discuss how we could help {{business_name}} streamline appointments?

Best regards,
{{sender_name}}
{{company_name}}`
    },
    professional: {
        subject: "Professional Website Solution for {{business_name}}",
        content: `Hello,

I noticed {{business_name}} doesn't have a website, and I specialize in creating professional online presences for businesses in your industry.

A custom website could help you:
• Showcase your expertise and services
• Accept online consultations
• Share client testimonials
• Build credibility in your field
• Generate leads 24/7

I'd be happy to create a free mock-up showing how your professional website could look. No obligation - just a chance to see the potential.

Would you like to schedule a quick 15-minute Zoom call to discuss how we could help {{business_name}} establish a strong online presence?

Best regards,
{{sender_name}}
{{company_name}}`
    },
    custom: {
        subject: "Website Development for {{business_name}}",
        content: `Hello,

I noticed {{business_name}} doesn't currently have a website. In today's digital age, this represents a significant business opportunity.

As a web developer specializing in {{business_type}} businesses, I can help you:
• Establish a professional online presence
• Appear in Google searches for '{{business_type}} in {{location}}'
• Convert online visitors into paying customers
• Automate customer interactions

I'd love to create a free mock-up showing how your website could look. No obligation - just a chance to see the possibilities.

Would you like to schedule a quick 15-minute Zoom call to discuss how we could help {{business_name}} grow online?

Best regards,
{{sender_name}}
{{company_name}}`
    }
};

// Load template based on selected business type
function loadTemplate() {
    const type = document.getElementById('template-type').value;
    const template = templates[type];
    
    if (template) {
        document.getElementById('template-subject').value = template.subject;
        document.getElementById('template-content').value = template.content;
    }
}

// Save template changes
function saveTemplate() {
    const type = document.getElementById('template-type').value;
    const subject = document.getElementById('template-subject').value;
    const content = document.getElementById('template-content').value;
    
    templates[type] = {
        subject: subject,
        content: content
    };
    
    alert('Template saved successfully!');
}

// Send test email
async function testTemplate() {
    const type = document.getElementById('template-type').value;
    const subject = document.getElementById('template-subject').value;
    const content = document.getElementById('template-content').value;
    
    try {
        const response = await fetch('/api/send-test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: type,
                subject: subject,
                content: content
            })
        });
        
        if (response.ok) {
            alert('Test email sent successfully!');
        } else {
            alert('Error sending test email. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error sending test email. Please try again.');
    }
}
