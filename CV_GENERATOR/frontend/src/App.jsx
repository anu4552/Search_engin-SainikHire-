import { useState } from "react";
import axios from "axios";

function App() {
  const [formData, setFormData] = useState({
    name: "",
    role: "",
    email: "",
    phone: "",
    address: "",
    summary: "",
    education: "",
    experience: "",
    skills: "",
    projects: "",
    awards: ""
  });

  const [generatedCV, setGeneratedCV] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleGenerate = async () => {
    const payload = {
      name: formData.name,
      role: formData.role,
      email: formData.email,
      phone: formData.phone,
      address: formData.address,
      summary: formData.summary,
      experience: formData.experience,
      skills: formData.skills.split(",").map(s => s.trim()),
      education: formData.education,
      projects: formData.projects.split(",").map(p => p.trim()),
      awards: formData.awards.split(",").map(a => a.trim())
    };

    try {
      const response = await axios.post("http://localhost:5000/generate-cv", payload);
      setGeneratedCV(response.data.resume);
    } catch (error) {
      console.error("Error generating CV:", error);
      alert("Error generating CV. Check backend logs.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-blue-100">
      <nav className="bg-blue-700 text-white px-6 py-4 shadow-md">
        <h1 className="text-3xl font-bold">📝 CV Generator</h1>
      </nav>

      <div className="flex flex-col lg:flex-row p-6 gap-8">
        {/* Left Panel: Form */}
        <div className="lg:w-1/2 bg-white p-6 rounded-xl shadow-md">
          <h2 className="text-xl font-semibold mb-4 text-blue-700">Enter Your Details</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {[
              ["name", "Name"],
              ["role", "Role"],
              ["email", "Email"],
              ["phone", "Phone"],
              ["address", "Address"],
              ["education", "Education"],
              ["experience", "Experience"],
              ["skills", "Skills (comma-separated)"],
              ["projects", "Projects (comma-separated)"],
              ["awards", "Awards (comma-separated)"]
            ].map(([key, label]) => (
              <div key={key} className="flex flex-col">
                <label className="text-sm text-gray-700 font-medium">{label}</label>
                <input
                  name={key}
                  value={formData[key]}
                  onChange={handleChange}
                  className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
                />
              </div>
            ))}
            <div className="col-span-1 sm:col-span-2 flex flex-col">
              <label className="text-sm text-gray-700 font-medium">Professional Summary</label>
              <textarea
                name="summary"
                value={formData.summary}
                onChange={handleChange}
                rows={3}
                className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
            </div>
          </div>

          <div className="mt-6 text-center">
            <button
              onClick={handleGenerate}
              className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition"
            >
              🚀 Generate CV
            </button>
          </div>
        </div>

        
             {/* Output Section */}
        <div className="lg:w-1/2 bg-white p-6 rounded-xl shadow-md">
          <h2 className="text-xl font-semibold mb-4 text-green-700 text-center">Generated CV</h2>

          <div className="border border-gray-300 p-4 rounded-md h-[500px] overflow-y-auto bg-white text-gray-900 text-sm leading-relaxed">
            {generatedCV ? (
              <div className="space-y-4">
                <div className="text-center">
                  <h1 className="text-2xl font-bold">{formData.name}</h1>
                  <p className="text-base italic text-gray-600">{formData.role}</p>
                  <p className="text-sm text-gray-600">{formData.email} | {formData.phone}</p>
                  <p className="text-sm text-gray-600">{formData.address}</p>
                </div>

                <div>
                  <h2 className="text-lg font-medium text-blue-700 border-b pb-1">Summary</h2>
                  <p><strong>{formData.summary}</strong></p>
                </div>

                <div>
                  <h2 className="text-lg font-medium text-blue-700 border-b pb-1">Education</h2>
                  <p><strong>{formData.education}</strong></p>
                </div>

                <div>
                  <h2 className="text-lg font-medium text-blue-700 border-b pb-1">Experience</h2>
                  <p><strong>{formData.experience}</strong></p>
                </div>

                <div>
                  <h2 className="text-lg font-medium text-blue-700 border-b pb-1">Skills</h2>
                  <ul className="list-disc list-inside grid grid-cols-2">
                    {formData.skills.split(',').map((skill, i) => (
                      <li key={i}><strong>{skill.trim()}</strong></li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h2 className="text-lg font-medium text-blue-700 border-b pb-1">Projects</h2>
                  <ul className="list-disc list-inside">
                    {formData.projects.split(',').map((project, i) => (
                      <li key={i}><strong>{project.trim()}</strong></li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h2 className="text-lg font-medium text-blue-700 border-b pb-1">Awards</h2>
                  <ul className="list-disc list-inside">
                    {formData.awards.split(',').map((award, i) => (
                      <li key={i}><strong>{award.trim()}</strong></li>
                    ))}
                  </ul>
                </div>
              </div>
            ) : (
              <p className="text-gray-500 italic">Your CV will appear here after generation.</p>
            )}
          </div>

          {generatedCV && (
            <div className="text-center mt-4">
              <button
                onClick={() => {
                  const blob = new Blob([generatedCV], { type: "text/plain;charset=utf-8" });
                  const url = window.URL.createObjectURL(blob);
                  const link = document.createElement("a");
                  link.href = url;
                  link.download = "cv.txt";
                  link.click();
                }}
                className="mt-4 px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition"
              >
                📥 Download as .txt
              </button>
            </div>
          )}
        </div>
      </div> 
    </div>
  );
}

export default App;


