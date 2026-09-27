const fs = require('fs');
const path = require('path');

const rootDir = path.join(__dirname, '..');
const headerTemplate = fs.readFileSync(path.join(rootDir, 'components/header.html'), 'utf8');
const mobileMenuTemplate = fs.readFileSync(path.join(rootDir, 'components/mobile-menu.html'), 'utf8');

const htmlFiles = fs.readdirSync(rootDir).filter(f => f.endsWith('.html'));

htmlFiles.forEach(fileName => {
  const filePath = path.join(rootDir, fileName);
  let content = fs.readFileSync(filePath, 'utf8');

  let homeActive = (fileName === 'index.html') ? 'active' : '';
  let aboutActive = (fileName === 'about-us.html') ? 'active' : '';
  let servicesActive = (fileName === 'services.html') ? 'active' : '';
  let knowledgeActive = (fileName === 'knowledge-base.html' || fileName.includes('calculator')) ? 'active' : '';
  let blogActive = (fileName === 'blog.html' || fileName.includes('tax') && !fileName.includes('calculator') && !fileName.includes('services') && !fileName.includes('consultant')) ? 'active' : '';
  let careerActive = (fileName === 'career.html') ? 'active' : '';
  let contactActive = (fileName === 'contact-us.html') ? 'active' : '';

  let pageHeader = headerTemplate
    .replace('{{NAV_HOME_ACTIVE}}', homeActive)
    .replace('{{NAV_ABOUT_ACTIVE}}', aboutActive)
    .replace('{{NAV_SERVICES_ACTIVE}}', servicesActive)
    .replace('{{NAV_GST_ACTIVE}}', '')
    .replace('{{NAV_KNOWLEDGE_ACTIVE}}', knowledgeActive)
    .replace('{{NAV_BLOG_ACTIVE}}', blogActive)
    .replace('{{NAV_CAREER_ACTIVE}}', careerActive)
    .replace('{{NAV_CONTACT_ACTIVE}}', contactActive);

  let pageMobileMenu = mobileMenuTemplate
    .replace('{{MOBILE_HOME_ACTIVE}}', homeActive)
    .replace('{{MOBILE_ABOUT_ACTIVE}}', aboutActive)
    .replace('{{MOBILE_SERVICES_ACTIVE}}', servicesActive)
    .replace('{{MOBILE_KNOWLEDGE_ACTIVE}}', knowledgeActive)
    .replace('{{MOBILE_BLOG_ACTIVE}}', blogActive)
    .replace('{{MOBILE_CAREER_ACTIVE}}', careerActive)
    .replace('{{MOBILE_CONTACT_ACTIVE}}', contactActive);

  if (content.includes('<header')) {
    content = content.replace(/<header[\s\S]*?<\/header>/, pageHeader);
  }

  if (content.includes('id="mobileMenu"')) {
    content = content.replace(/<div class="offcanvas offcanvas-end text-bg-dark"[\s\S]*?<\/div>\s*<\/div>\s*<\/div>/, pageMobileMenu);
  }

  if (!content.includes('header-component.js')) {
    content = content.replace('</body>', '  <script src="assets/js/header-component.js"></script>\n</body>');
  }

  fs.writeFileSync(filePath, content, 'utf8');
});

console.log('Master sync complete. Synchronized unified header across all ' + htmlFiles.length + ' HTML files.');
