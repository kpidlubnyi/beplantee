from fastapi import APIRouter
from app.schemas.faq import FAQResponse

router = APIRouter(prefix="/faq", tags=["faq"])

@router.get("", response_model=FAQResponse)
def get_faq():
    """
    Zwraca informację FAQ
    """
    faq_data = {
        "categories": [
            {
                "title": "General Questions",
                "items": [
                    {
                        "question": "What is BePlantee?",
                        "answer": "BePlantee is a plant management application that helps you track and care for your houseplants. You can manage your plant collection, keep track of watering and sunlight schedules, and access care information for various plant species."
                    },
                    {
                        "question": "Is BePlantee free to use?",
                        "answer": "Yes, BePlantee is currently free to use for all users. We may introduce premium features in the future, but the core functionality will remain free."
                    },
                    {
                        "question": "Do I need to create an account to use BePlantee?",
                        "answer": "Yes, you need to create an account to use BePlantee. This allows us to save your plant collection and care history."
                    }
                ]
            },
            {
                "title": "Account Management",
                "items": [
                    {
                        "question": "How do I create an account?",
                        "answer": "To create an account, click the \"Register\" button on the home page and fill in the required information: username, email, and password. Your password must be at least 8 characters long and include uppercase letters, lowercase letters, numbers, and special characters."
                    },
                    {
                        "question": "I forgot my password. How can I reset it?",
                        "answer": "Click on the \"Forgot Password\" link on the login page. Enter your email address, and we'll send you instructions on how to reset your password."
                    },
                    {
                        "question": "How secure is my password?",
                        "answer": "Your password is securely hashed using bcrypt, which is a strong cryptographic hashing algorithm. We never store your actual password, only a secure hash of it."
                    },
                    {
                        "question": "Can I change my username or email?",
                        "answer": "Currently, you cannot change your username after registration. If you need to update your email, please contact our support team."
                    }
                ]
            },
            {
                "title": "Plant Management",
                "items": [
                    {
                        "question": "How do I add a new plant to my collection?",
                        "answer": "To add a new plant, click the \"Add Plant\" button on your dashboard. Select the type of plant from the dropdown menu, give it a name (up to 20 characters), and optionally upload a photo of your plant."
                    },
                    {
                        "question": "Can I upload a photo of my plant?",
                        "answer": "Yes, you can upload a photo when adding a new plant or update the photo later. Supported file formats include JPEG, PNG, and GIF. Photos are automatically optimized and resized for better performance."
                    },
                    {
                        "question": "What if I don't have a photo of my plant?",
                        "answer": "If you don't upload a photo, a default plant image will be used instead. You can always add a photo later."
                    },
                    {
                        "question": "How do I record watering my plant?",
                        "answer": "Open the details page for your plant and click the \"Water\" button. This will record the current date and time as the last watering date for that plant."
                    },
                    {
                        "question": "How do I record giving my plant sunlight?",
                        "answer": "Open the details page for your plant and click the \"Sunlight\" button. This will record the current date and time as the last sunlight date for that plant."
                    },
                    {
                        "question": "How does BePlantee determine when my plants need watering?",
                        "answer": "BePlantee uses the plant's species information to determine optimal watering frequency. Plants are categorized as requiring frequent (every 2 days), average (every 5 days), or minimum (every 10 days) watering. The app calculates a watering level from 1-5 based on how long it's been since the last watering relative to the recommended interval."
                    },
                    {
                        "question": "How does the sunlight tracking work?",
                        "answer": "BePlantee tracks when you last exposed your plant to sunlight. If it's been more than 24 hours since the last recorded sun exposure, the app will indicate that your plant needs sunlight (level 5). Otherwise, it will show that your plant has received adequate sunlight (level 1)."
                    },
                    {
                        "question": "Can I edit the information about my plants?",
                        "answer": "Yes, you can edit the name of your plant, change its photo, or even change the plant type if you misidentified it initially."
                    },
                    {
                        "question": "How do I delete a plant from my collection?",
                        "answer": "On the plant details page, look for the \"Delete\" or \"Remove\" button. After confirming, the plant will be permanently removed from your collection."
                    }
                ]
            },
            {
                "title": "Troubleshooting",
                "items": [
                    {
                        "question": "The app says \"Plant not found in database\" when I try to add a new plant",
                        "answer": "This error occurs when the plant type you selected no longer exists in our database. Please try selecting a different plant type or contact support if the issue persists."
                    },
                    {
                        "question": "I can't upload a photo of my plant",
                        "answer": "Make sure your photo is in a supported format (JPEG, PNG, or GIF) and doesn't exceed the maximum file size limit. Also, check your internet connection, as poor connectivity can affect file uploads."
                    },
                    {
                        "question": "The watering or sunlight level isn't updating after I click the button",
                        "answer": "Try refreshing the page. If the problem persists, log out and log back in. If you still experience issues, please contact our support team."
                    },
                    {
                        "question": "I can't log in even though I'm using the correct credentials",
                        "answer": "Make sure you're using the correct username (not email) to log in. If you've forgotten your password, use the \"Forgot Password\" feature. If you still can't log in, contact our support team."
                    }
                ]
            },
            {
                "title": "Technical Questions",
                "items": [
                    {
                        "question": "What browsers are supported?",
                        "answer": "BePlantee works on all modern browsers, including Chrome, Firefox, Safari, and Edge. For the best experience, we recommend using the latest version of your preferred browser."
                    },
                    {
                        "question": "Is my data backed up?",
                        "answer": "Yes, all your plant data is stored in our secure database and backed up regularly. However, we recommend keeping your own records of particularly important plant care information."
                    },
                    {
                        "question": "Do you have an API?",
                        "answer": "Currently, our API is for internal use only. If you're interested in integrating with BePlantee, please contact us for more information."
                    }
                ]
            },
            {
                "title": "Privacy & Security",
                "items": [
                    {
                        "question": "What data does BePlantee collect about me?",
                        "answer": "BePlantee collects your username, email, and information about your plants (including photos you upload). We do not collect any other personal information."
                    },
                    {
                        "question": "Are my plant photos stored securely?",
                        "answer": "Yes, all uploaded photos are stored securely on our servers. We optimize these images for performance while maintaining privacy."
                    },
                    {
                        "question": "Does BePlantee share my data with third parties?",
                        "answer": "No, we do not share your personal information or plant data with any third parties. Your data is used only to provide you with the BePlantee service."
                    },
                    {
                        "question": "How can I delete my account and all my data?",
                        "answer": "To delete your account, please contact our support team. Upon account deletion, all your personal information and plant data will be permanently removed from our systems."
                    }
                ]
            },
            {
                "title": "Contact & Support",
                "items": [
                    {
                        "question": "How can I contact support?",
                        "answer": "If you have any questions, issues, or feedback, please email us at support@beplantee.com. We aim to respond to all inquiries within 48 hours."
                    },
                    {
                        "question": "Where can I report bugs or suggest features?",
                        "answer": "You can report bugs or suggest features by emailing support@beplantee.com. We appreciate your feedback and continuously work to improve BePlantee."
                    },
                    {
                        "question": "Do you offer developer documentation?",
                        "answer": "Currently, we don't offer public developer documentation, as our API is for internal use only. If you're a developer interested in contributing to BePlantee, please contact us."
                    }
                ]
            }
        ]
    }
    
    return faq_data
