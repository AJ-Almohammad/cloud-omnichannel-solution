import React, { useState, useEffect } from 'react';
import jsPDF from 'jspdf';
import { 
  User, 
  Briefcase, 
  Mail, 
  Phone, 
  MapPin, 
  Calendar,
  Award,
  Code,
  Globe,
  Github,
  Linkedin,
  ChevronRight,
  Star,
  TrendingUp,
  Zap,
  Cloud,
  Server,
  Database,
  Settings,
  BarChart3,
  Shield,
  Layers,
  Network
} from 'lucide-react';

const CloudOmnichannelApp = () => {
  const [activeSection, setActiveSection] = useState('overview');
  const [orders, setOrders] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);

  // Mock API calls for demonstration
  const fetchOrders = async () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setOrders([
        { id: 'ORD-2024-001', customer: 'Alice Johnson', amount: 129.99, status: 'delivered', channel: 'online' },
        { id: 'ORD-2024-002', customer: 'Bob Smith', amount: 299.50, status: 'processing', channel: 'in_store' },
        { id: 'ORD-2024-003', customer: 'Carol Williams', amount: 79.99, status: 'shipped', channel: 'mobile_app' },
        { id: 'ORD-2024-004', customer: 'David Brown', amount: 199.99, status: 'confirmed', channel: 'online' },
      ]);
      setStats({
        totalOrders: 247,
        totalRevenue: 45678.90,
        averageOrderValue: 184.86,
        conversionRate: 3.2
      });
      setLoading(false);
    }, 1000);
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const CVSection = () => (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 text-white overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500 rounded-full opacity-10 animate-pulse"></div>
        <div className="absolute top-1/2 -left-32 w-64 h-64 bg-purple-500 rounded-full opacity-10 animate-bounce"></div>
        <div className="absolute bottom-20 right-1/4 w-48 h-48 bg-cyan-500 rounded-full opacity-10 animate-ping"></div>
      </div>

      <div className="relative z-10 container mx-auto px-6 py-12">
        {/* Header Section */}
        <div className="text-center mb-16">
          <div className="relative inline-block">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-600 blur-2xl opacity-30 animate-pulse"></div>
            <h1 className="relative text-6xl font-bold bg-gradient-to-r from-blue-400 via-purple-500 to-cyan-400 bg-clip-text text-transparent mb-4">
              Amer Almohammad
            </h1>
          </div>
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-3 rounded-full inline-block shadow-2xl transform hover:scale-105 transition-all duration-300">
            <h2 className="text-2xl font-semibold">Junior Solution Architect</h2>
          </div>
          
          {/* Contact Info */}
          <div className="mt-8 flex flex-wrap justify-center gap-6 text-gray-300">
            <div className="flex items-center gap-2 hover:text-blue-400 transition-colors">
              <Mail className="w-5 h-5" />
              <span>ajaber1973@web.de</span>
            </div>
            <div className="flex items-center gap-2 hover:text-blue-400 transition-colors">
              <Phone className="w-5 h-5" />
              <span>+49-160-75-85-772</span>
            </div>
            <div className="flex items-center gap-2 hover:text-blue-400 transition-colors">
              <MapPin className="w-5 h-5" />
              <span>Berlin, Germany</span>
            </div>
            <a href="https://linkedin.com/in/amer-almohammad-27161534" className="flex items-center gap-2 hover:text-blue-400 transition-colors">
              <Linkedin className="w-5 h-5" />
              <span>LinkedIn</span>
            </a>
            <a href="https://github.com/AJ-Almohammad" className="flex items-center gap-2 hover:text-blue-400 transition-colors">
              <Github className="w-5 h-5" />
              <span>GitHub</span>
            </a>
          </div>
        </div>

        {/* Profile Section */}
        <div className="mb-16">
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-white/20 hover:bg-white/15 transition-all duration-300">
            <div className="flex items-center gap-4 mb-6">
              <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-3 rounded-2xl">
                <User className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-3xl font-bold text-white">Professional Profile</h3>
            </div>
            <p className="text-gray-200 text-lg leading-relaxed">
              <span className="text-blue-400 font-semibold">Junior Cloud Architect</span> with one year of remote experience in crafting and implementing 
              cloud solutions across diverse platforms. Well-versed in <span className="text-purple-400 font-semibold">cloud-native technologies and DevOps practices</span>, 
              with a focus on improving system scalability, performance, and automation. Proven ability to collaborate with cross-functional teams to enhance 
              cloud infrastructure and support strategic initiatives aligned with business needs. Committed to continuous learning and delivering efficient, 
              <span className="text-cyan-400 font-semibold">future-ready cloud environments</span>.
            </p>
            
            {/* Key Highlights */}
            <div className="mt-6 grid md:grid-cols-3 gap-4">
              <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 rounded-xl p-4 border border-blue-400/30">
                <Cloud className="w-8 h-8 text-blue-400 mb-2" />
                <h4 className="font-semibold text-blue-300">Cloud Native</h4>
                <p className="text-sm text-gray-300">AWS, Azure, GCP knowledgeable</p>
              </div>
              <div className="bg-gradient-to-br from-purple-500/20 to-purple-600/20 rounded-xl p-4 border border-purple-400/30">
                <Layers className="w-8 h-8 text-purple-400 mb-2" />
                <h4 className="font-semibold text-purple-300">Architecture</h4>
                <p className="text-sm text-gray-300">Scalable system design</p>
              </div>
              <div className="bg-gradient-to-br from-cyan-500/20 to-cyan-600/20 rounded-xl p-4 border border-cyan-400/30">
                <Settings className="w-8 h-8 text-cyan-400 mb-2" />
                <h4 className="font-semibold text-cyan-300">DevOps</h4>
                <p className="text-sm text-gray-300">CI/CD & Automation</p>
              </div>
            </div>
          </div>
        </div>

        {/* Experience Section */}
        <div className="mb-16">
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-white/20">
            <div className="flex items-center gap-4 mb-8">
              <div className="bg-gradient-to-r from-green-500 to-blue-600 p-3 rounded-2xl">
                <Briefcase className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-3xl font-bold text-white">Professional Experience</h3>
            </div>
            
            <div className="space-y-8">
              {/* Current Role - Tailored for Solution Architect */}
              <div className="relative pl-8 border-l-4 border-gradient-to-b from-blue-500 to-purple-600">
                <div className="absolute -left-3 top-0 w-6 h-6 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full border-4 border-slate-900"></div>
                <div className="bg-gradient-to-r from-blue-500/10 to-purple-600/10 rounded-2xl p-6 border border-blue-400/20">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h4 className="text-2xl font-bold text-blue-400">Cloud Solution Engineer (Winfrox)</h4>
                      <p className="text-purple-300 text-lg font-semibold">Junior Solution Architect Position</p>
                      <p className="text-gray-400">Remote (Winfrox)</p>
                    </div>
                    <span className="bg-green-500/20 text-green-400 px-4 py-2 rounded-full text-sm font-semibold">
                      April 2025 - Present
                    </span>
                  </div>
                  <div className="grid md:grid-cols-2 gap-4 mb-4">
                    <div className="bg-slate-800/50 rounded-xl p-4">
                      <h5 className="text-cyan-400 font-semibold mb-2">Technical Leadership</h5>
                      <ul className="text-gray-300 text-sm space-y-1">
                        <li>• Omnichannel solution architecture design</li>
                        <li>• Full-stack development coordination</li>
                        <li>• Cloud-native technology implementation</li>
                      </ul>
                    </div>
                    <div className="bg-slate-800/50 rounded-xl p-4">
                      <h5 className="text-purple-400 font-semibold mb-2">Project Lifecycle</h5>
                      <ul className="text-gray-300 text-sm space-y-1">
                        <li>• Customer requirement analysis</li>
                        <li>• Solution planning & implementation</li>
                        <li>• Partner & stakeholder coordination</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              {/* Previous Experience */}
              <div className="relative pl-8 border-l-4 border-gray-600">
                <div className="absolute -left-3 top-0 w-6 h-6 bg-gray-600 rounded-full border-4 border-slate-900"></div>
                <div className="bg-gray-800/30 rounded-2xl p-6 border border-gray-600/20">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h4 className="text-xl font-bold text-gray-200">Regional Business Manager</h4>
                      <p className="text-gray-300 font-semibold">SLB (Schlumberger) Oilfield Services</p>
                      <p className="text-gray-400">Congo, Gabon, Cameroon, Equatorial Guinea</p>
                    </div>
                    <span className="text-gray-400 text-sm">2006 - 2018</span>
                  </div>
                  <div className="grid md:grid-cols-3 gap-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-400">15%</div>
                      <div className="text-sm text-gray-400">Downtime Reduction</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-400">$5M+</div>
                      <div className="text-sm text-gray-400">Contracts Secured</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-purple-400">30%</div>
                      <div className="text-sm text-gray-400">Performance Boost</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Education & Certifications */}
        <div className="mb-16">
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-white/20">
            <div className="flex items-center gap-4 mb-8">
              <div className="bg-gradient-to-r from-yellow-500 to-orange-600 p-3 rounded-2xl">
                <Award className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-3xl font-bold text-white">Education & Certifications</h3>
            </div>
            
            <div className="grid md:grid-cols-2 gap-8">
              {/* Education */}
              <div>
                <h4 className="text-xl font-bold text-yellow-400 mb-4">Education</h4>
                <div className="space-y-4">
                  <div className="bg-gradient-to-r from-yellow-500/10 to-orange-500/10 rounded-xl p-4 border border-yellow-400/20">
                    <h5 className="font-bold text-yellow-300">AWS Cloud Engineering</h5>
                    <p className="text-orange-300">DCI Digital Career Institute GmbH</p>
                    <p className="text-gray-400 text-sm">2024 - 2025 | Berlin, Germany</p>
                  </div>
                  <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-xl p-4 border border-blue-400/20">
                    <h5 className="font-bold text-blue-300">Bachelor of Computer Science</h5>
                    <p className="text-purple-300">University of the People</p>
                    <p className="text-gray-400 text-sm">2020 - 2024 | Online</p>
                  </div>
                </div>
              </div>
              
              {/* Certifications */}
              <div>
                <h4 className="text-xl font-bold text-green-400 mb-4">Certifications</h4>
                <div className="space-y-3">
                  {[
                    { name: "AWS Solution Architect Professional", expires: "Aug 2028", level: "Professional" },
                    { name: "AWS Cloud Practitioner Associate", expires: "Aug 2028", level: "Associate" },
                    { name: "HashiCorp Terraform Associate", expires: "Apr 2027", level: "Associate" }
                  ].map((cert, index) => (
                    <div key={index} className="bg-gradient-to-r from-green-500/10 to-blue-500/10 rounded-xl p-4 border border-green-400/20 flex items-center justify-between">
                      <div>
                        <h5 className="font-semibold text-green-300">{cert.name}</h5>
                        <p className="text-gray-400 text-sm">Expires: {cert.expires}</p>
                      </div>
                      <div className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-sm font-semibold">
                        {cert.level}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Skills Section */}
        <div className="mb-16">
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-white/20">
            <div className="flex items-center gap-4 mb-8">
              <div className="bg-gradient-to-r from-cyan-500 to-blue-600 p-3 rounded-2xl">
                <Code className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-3xl font-bold text-white">Technical Skills</h3>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[
                { category: "Cloud Platforms", skills: ["AWS", "Azure", "Google Cloud"], color: "from-blue-500 to-cyan-500" },
                { category: "Infrastructure as Code", skills: ["Terraform", "CloudFormation", "Ansible"], color: "from-purple-500 to-pink-500" },
                { category: "Programming", skills: ["Python", "Java", "SQL", "JavaScript"], color: "from-green-500 to-emerald-500" },
                { category: "DevOps Tools", skills: ["Docker", "Kubernetes", "Jenkins", "Git"], color: "from-orange-500 to-red-500" }
              ].map((skillGroup, index) => (
                <div key={index} className={`bg-gradient-to-br ${skillGroup.color} bg-opacity-10 rounded-2xl p-6 border border-white/20`}>
                  <h4 className="font-bold text-white mb-4">{skillGroup.category}</h4>
                  <div className="space-y-2">
                    {skillGroup.skills.map((skill, skillIndex) => (
                      <div key={skillIndex} className="bg-white/10 rounded-lg px-3 py-2 text-sm text-gray-200 text-center hover:bg-white/20 transition-colors">
                        {skill}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
	{/* Project Achievements Section - NEW */}
        <div className="mb-16">
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-white/20">
            <div className="flex items-center gap-4 mb-8">
              <div className="bg-gradient-to-r from-emerald-500 to-teal-600 p-3 rounded-2xl">
                <Star className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-3xl font-bold text-white">Project Achievements</h3>
            </div>
            
            <div className="bg-gradient-to-r from-emerald-500/10 to-teal-500/10 rounded-2xl p-6 border border-emerald-400/20">
              <h4 className="text-2xl font-bold text-emerald-400 mb-4">Cloud Omnichannel Solution</h4>
              <p className="text-gray-200 text-lg mb-6">
                Architected and developed a comprehensive enterprise-grade omnichannel solution demonstrating 
                full-stack development expertise and cloud-native architectural patterns.
              </p>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="bg-slate-800/50 rounded-xl p-4">
                  <h5 className="text-emerald-400 font-semibold mb-2">Backend Architecture</h5>
                  <ul className="text-gray-300 text-sm space-y-1">
                    <li>• FastAPI with modular design patterns</li>
                    <li>• RESTful API with OpenAPI documentation</li>
                    <li>• Comprehensive health monitoring</li>
                    <li>• Professional logging and error handling</li>
                  </ul>
                </div>
                
                <div className="bg-slate-800/50 rounded-xl p-4">
                  <h5 className="text-teal-400 font-semibold mb-2">Frontend Excellence</h5>
                  <ul className="text-gray-300 text-sm space-y-1">
                    <li>• Modern React 18 with hooks</li>
                    <li>• Tailwind CSS with custom animations</li>
                    <li>• Responsive, mobile-first design</li>
                    <li>• Interactive data visualizations</li>
                  </ul>
                </div>
                
                <div className="bg-slate-800/50 rounded-xl p-4">
                  <h5 className="text-cyan-400 font-semibold mb-2">DevOps Integration</h5>
                  <ul className="text-gray-300 text-sm space-y-1">
                    <li>• Docker containerization</li>
                    <li>• GitHub Actions CI/CD pipeline</li>
                    <li>• Automated testing suites</li>
                    <li>• AWS deployment ready</li>
                  </ul>
                </div>
              </div>
              
              <div className="mt-6 grid md:grid-cols-4 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-emerald-400">Full-Stack</div>
                  <div className="text-sm text-gray-400">Architecture</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-teal-400">8 Endpoints</div>
                  <div className="text-sm text-gray-400">API Coverage</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-cyan-400">Multi-Channel</div>
                  <div className="text-sm text-gray-400">Order System</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-blue-400">Cloud Ready</div>
                  <div className="text-sm text-gray-400">Deployment</div>
                </div>
              </div>
              
              <div className="mt-4 text-center">
                <a href="https://github.com/AJ-Almohammad/cloud-omnichannel-solution" 
                   className="inline-flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-2 px-6 rounded-xl transition-colors">
                  <Github className="w-5 h-5" />
                  View Project Source
                </a>
              </div>
            </div>
          </div>
        </div>
        {/* Languages Section */}
        <div className="mb-16">
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-white/20">
            <div className="flex items-center gap-4 mb-8">
              <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-3 rounded-2xl">
                <Globe className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-3xl font-bold text-white">Languages</h3>
            </div>
            
            <div className="grid md:grid-cols-3 gap-6">
              {[
                { language: "Arabic", level: "Native", proficiency: 100, color: "bg-emerald-500" },
                { language: "English", level: "Professional", proficiency: 90, color: "bg-blue-500" },
                { language: "German", level: "Elementary", proficiency: 60, color: "bg-yellow-500" }
              ].map((lang, index) => (
                <div key={index} className="bg-gray-800/50 rounded-2xl p-6 border border-gray-600/30">
                  <div className="flex justify-between items-center mb-4">
                    <h4 className="font-bold text-white text-lg">{lang.language}</h4>
                    <span className="text-gray-300 text-sm">{lang.level}</span>
                  </div>
                  <div className="bg-gray-700 rounded-full h-3 overflow-hidden">
                    <div 
                      className={`${lang.color} h-full rounded-full transition-all duration-1000 ease-out`}
                      style={{ width: `${lang.proficiency}%` }}
                    ></div>
                  </div>
                  <div className="text-right text-gray-400 text-sm mt-2">{lang.proficiency}%</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Call to Action */}
        <div className="text-center">
          <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-600 rounded-3xl p-8 shadow-2xl">
            <h3 className="text-3xl font-bold text-white mb-4">Ready to Architect Your Cloud Solutions</h3>
            <p className="text-blue-100 text-lg mb-6">
              Passionate about building scalable, efficient, and innovative cloud architectures that drive business success.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
  <button 
    onClick={() => {
  const pdf = new jsPDF();
  
  // Set font and colors
  pdf.setFont("helvetica");
  
  // Header
  pdf.setFontSize(20);
  pdf.setTextColor(59, 130, 246); // Blue color
  pdf.text("AMER ALMOHAMMAD", 20, 25);
  
  pdf.setFontSize(16);
  pdf.setTextColor(147, 51, 234); // Purple color
  pdf.text("Junior Solution Architect", 20, 35);
  
  // Contact Information
  pdf.setFontSize(10);
  pdf.setTextColor(0, 0, 0); // Black color
  pdf.text("Email: ajaber1973@web.de | Phone: +49-160-75-85-772 | Berlin, Germany", 20, 45);
  pdf.text("LinkedIn: linkedin.com/in/amer-almohammad-27161534", 20, 52);
  pdf.text("GitHub: https://github.com/AJ-Almohammad", 20, 59);
  
  // Professional Profile
  pdf.setFontSize(14);
  pdf.setTextColor(59, 130, 246);
  pdf.text("PROFESSIONAL PROFILE", 20, 75);
  
  pdf.setFontSize(10);
  pdf.setTextColor(0, 0, 0);
  const profileText = "Junior Cloud Architect with one year of remote experience in crafting and implementing cloud solutions across diverse platforms. Well-versed in cloud-native technologies and DevOps practices, with a focus on improving system scalability, performance, and automation.";
  const splitProfile = pdf.splitTextToSize(profileText, 170);
  pdf.text(splitProfile, 20, 85);
  
  // Experience
  pdf.setFontSize(14);
  pdf.setTextColor(59, 130, 246);
  pdf.text("PROFESSIONAL EXPERIENCE", 20, 110);
  
  pdf.setFontSize(12);
  pdf.setTextColor(0, 0, 0);
  pdf.text("Cloud Solution Engineer - Winfrox Org", 20, 122);
  pdf.setFontSize(10);
  pdf.text("April 2025 - Present | Remote (Winfrox)", 20, 130);
  pdf.text("• Omnichannel solution architecture design", 25, 138);
  pdf.text("• Full-stack development coordination", 25, 145);
  pdf.text("• Cloud-native technology implementation", 25, 152);
  
  pdf.setFontSize(12);
  pdf.text("Regional Business Manager - SLB Schlumberger", 20, 165);
  pdf.setFontSize(10);
  pdf.text("2006 - 2018 | Congo, Gabon, Cameroon, Equatorial Guinea", 20, 173);
  pdf.text("• 15% downtime reduction, $5M+ contracts secured, 30% performance boost", 25, 181);
  
  // Education & Certifications
  pdf.setFontSize(14);
  pdf.setTextColor(59, 130, 246);
  pdf.text("EDUCATION & CERTIFICATIONS", 20, 200);
  
  pdf.setFontSize(10);
  pdf.setTextColor(0, 0, 0);
  pdf.text("AWS Cloud Engineering - DCI Digital Career Institute GmbH (2024-2025)", 20, 212);
  pdf.text("Bachelor of Computer Science - University of the People (2020-2024)", 20, 220);
  
  pdf.text("AWS Solution Architect Professional (Expires: Aug 2028)", 20, 232);
  pdf.text("AWS Cloud Practitioner Associate (Expires: Aug 2028)", 20, 239);
  pdf.text("HashiCorp Terraform Associate (Expires: Apr 2027)", 20, 246);
  
  // Skills
  pdf.setFontSize(14);
  pdf.setTextColor(59, 130, 246);
  pdf.text("TECHNICAL SKILLS", 20, 265);
  
  pdf.setFontSize(10);
  pdf.setTextColor(0, 0, 0);
  pdf.text("Cloud Platforms: AWS focused, Azure & GCP knowledgeable", 20, 275);
  pdf.text("Programming: Python, Java, SQL, JavaScript", 20, 282);
  pdf.text("DevOps Tools: Docker, Kubernetes, Jenkins, Git, Terraform", 20, 289);
  
  // Save the PDF
  pdf.save('Amer_Almohammad_CV.pdf');
}}

    className="bg-white text-blue-600 font-bold py-3 px-8 rounded-xl hover:bg-blue-50 transition-colors shadow-lg"
  >
    Download CV
  </button>
  <button 
    onClick={() => {
      // Show contact information in an alert and copy to clipboard
      const contactInfo = `Amer Almohammad
📧 Email: ajaber1973@web.de
📱 Phone: +49-160-75-85-772
📍 Location: Berlin, Germany
💼 LinkedIn: linkedin.com/in/amer-almohammad-27161534
👨‍💻 GitHub: https://github.com/AJ-Almohammad`;
      
      // Copy to clipboard
      navigator.clipboard.writeText(contactInfo).then(() => {
        alert(`Contact Information:\n\n${contactInfo}\n\n✅ Copied to clipboard!`);
      }).catch(() => {
        alert(`Contact Information:\n\n${contactInfo}`);
      });
    }}
    className="bg-transparent border-2 border-white text-white font-bold py-3 px-8 rounded-xl hover:bg-white hover:text-blue-600 transition-colors"
  >
    Contact Me
  </button>
</div>
          </div>
        </div>
      </div>
    </div>
  );

  const DashboardSection = () => (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Cloud Omnichannel Dashboard</h1>
          <p className="text-gray-600">Comprehensive order management across all sales channels</p>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-2xl p-6 shadow-lg border border-blue-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-blue-600 text-sm font-semibold">Total Orders</p>
                  <p className="text-3xl font-bold text-gray-900">{stats.totalOrders}</p>
                </div>
                <div className="bg-blue-100 p-3 rounded-xl">
                  <BarChart3 className="w-8 h-8 text-blue-600" />
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-2xl p-6 shadow-lg border border-green-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-600 text-sm font-semibold">Total Revenue</p>
                  <p className="text-3xl font-bold text-gray-900">€{stats.totalRevenue.toLocaleString()}</p>
                </div>
                <div className="bg-green-100 p-3 rounded-xl">
                  <TrendingUp className="w-8 h-8 text-green-600" />
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-2xl p-6 shadow-lg border border-purple-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-purple-600 text-sm font-semibold">Avg Order Value</p>
                  <p className="text-3xl font-bold text-gray-900">€{stats.averageOrderValue}</p>
                </div>
                <div className="bg-purple-100 p-3 rounded-xl">
                  <Star className="w-8 h-8 text-purple-600" />
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-2xl p-6 shadow-lg border border-orange-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-orange-600 text-sm font-semibold">Conversion Rate</p>
                  <p className="text-3xl font-bold text-gray-900">{stats.conversionRate}%</p>
                </div>
                <div className="bg-orange-100 p-3 rounded-xl">
                  <Zap className="w-8 h-8 text-orange-600" />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Orders Table */}
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Recent Orders</h2>
              <button 
                onClick={fetchOrders}
                className="bg-blue-600 text-white px-6 py-2 rounded-xl hover:bg-blue-700 transition-colors flex items-center gap-2"
              >
                <Server className="w-4 h-4" />
                Refresh Data
              </button>
            </div>
          </div>
          
          {loading ? (
            <div className="p-12 text-center">
              <div className="animate-spin w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
              <p className="text-gray-600">Loading orders...</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order ID</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Channel</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {orders.map((order) => (
                    <tr key={order.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{order.id}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{order.customer}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">€{order.amount}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          order.status === 'delivered' ? 'bg-green-100 text-green-800' :
                          order.status === 'processing' ? 'bg-yellow-100 text-yellow-800' :
                          order.status === 'shipped' ? 'bg-blue-100 text-blue-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {order.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          order.channel === 'online' ? 'bg-blue-100 text-blue-800' :
                          order.channel === 'in_store' ? 'bg-green-100 text-green-800' :
                          'bg-purple-100 text-purple-800'
                        }`}>
                          {order.channel}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/10 backdrop-blur-lg border-b border-white/20">
        <div className="container mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="text-2xl font-bold text-white">
              Cloud Omnichannel Solution
            </div>
            <div className="flex space-x-1 bg-white/10 rounded-full p-1">
              <button
                onClick={() => setActiveSection('overview')}
                className={`px-6 py-2 rounded-full font-medium transition-all duration-300 ${
                  activeSection === 'overview' 
                    ? 'bg-white text-blue-600 shadow-lg' 
                    : 'text-white hover:bg-white/10'
                }`}
              >
                Profile
              </button>
              <button
                onClick={() => setActiveSection('dashboard')}
                className={`px-6 py-2 rounded-full font-medium transition-all duration-300 ${
                  activeSection === 'dashboard' 
                    ? 'bg-white text-blue-600 shadow-lg' 
                    : 'text-white hover:bg-white/10'
                }`}
>
               Dashboard
             </button>
           </div>
         </div>
       </div>
     </nav>

     {/* Content */}
     <div className="pt-20">
       {activeSection === 'overview' && <CVSection />}
       {activeSection === 'dashboard' && <DashboardSection />}
     </div>
   </div>
 );
};

export default CloudOmnichannelApp;