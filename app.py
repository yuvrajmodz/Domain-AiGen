from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import time
import whois
import os

app = Flask(__name__)

#╔════════════════════════════╗
#║                                            
#║    𝗖𝗼𝗽𝘆𝗿𝗶𝗴𝗵𝘁 © 𝟮𝟬𝟮𝟰 𝗬𝗨𝗩𝗥𝗔𝗝𝗠𝗢𝗗𝗭     
#║     𝗖𝗥𝗘𝗗𝗜𝗧: 𝐌𝐀𝐓𝐑𝐈𝐗 𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑      
#║                                            
#╚════════════════════════════╝

def check_domain_availability(domain):
    try:
        domain_info = whois.whois(domain)
        return domain_info.domain_name is None
    except Exception as e:
        return True

def extract_domains(prompt_text):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
        page = context.new_page()

        # Navigate to the target page
        page.goto("https://www.domain.com/domains/ai-domain-generator?endpoint=jarvis&flow=jdomainDFE#/jdomainDFE/1")

        # Fill in the prompt text in the specific textarea field
        textarea_selector = "textarea[aria-label='A website dedicated to paintings of pets and their humans...']"
        page.fill(textarea_selector, prompt_text)

        button_selector = "#domain-ai-mfe__name-finder__submit"
        page.click(button_selector)

        loading_selector = ".MuiSkeleton-root.MuiSkeleton-text.MuiSkeleton-pulse.css-z7erpk"
        page.wait_for_selector(loading_selector, state="visible") 
        page.wait_for_selector(loading_selector, state="hidden")

        page_content = page.content()

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(page_content, 'html.parser')

        domains = []
        domain_spans = soup.find_all("span", class_="MuiTypography-root MuiTypography-h3 MuiCardHeader-title css-e461jq")

        for span in domain_spans:
            domain_name = span.text.strip()
            domains.append(domain_name)

        available_domains = []
        for domain in domains:
            if check_domain_availability(domain):
                available_domains.append(domain)

        browser.close()

        return available_domains

@app.route('/Ai-GenDomain', methods=['GET'])
def ai_gen_domain():
    prompt = request.args.get('prompt', '')
    if not prompt:
        return jsonify({"error": "Prompt parameter is required."}), 400
        
# Request Url : http://domain.com/Ai-GenDomain?prompt=best%20short%20link%20domain

    available_domains = extract_domains(prompt)
    return jsonify({"available": available_domains})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5019))
    app.run(host='0.0.0.0', port=port, debug=True)
