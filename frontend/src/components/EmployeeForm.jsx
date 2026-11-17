
import { useEffect, useState } from "react";
import {
  createEmployee,
  updateEmployee,
  getDepartments,
  getProjects,
} from "../services/employeeService";

const initialForm = {
  employee_id: "",
  name: "",
  email: "",
  phone: "",
  salary: "",
  department: "",
  job_role: "",
  date_of_joining: "",
  projects: [],
  profile_image: null,
};

function EmployeeForm({ editingEmployee, onSaved, onCancel }) {
  const [form, setForm] = useState(initialForm);
  const [departments, setDepartments] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [optionsLoading, setOptionsLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [imagePreview, setImagePreview] = useState("");
  const [imageError, setImageError] = useState("");

  useEffect(() => {
    const loadOptions = async () => {
      try {
        const [departmentData, projectData] = await Promise.all([
          getDepartments(),
          getProjects(),
        ]);

        setDepartments(departmentData.results || departmentData);
        setProjects(projectData.results || projectData);
      } catch {
        setError("Unable to load departments and projects.");
      } finally {
        setOptionsLoading(false);
      }
    };

    loadOptions();
  }, []);

  useEffect(() => {
    if (editingEmployee) {
      setForm({
        employee_id: editingEmployee.employee_id || "",
        name: editingEmployee.name || "",
        email: editingEmployee.email || "",
        phone: editingEmployee.phone || "",
        salary: editingEmployee.salary || "",
        department: String(editingEmployee.department || ""),
        job_role: editingEmployee.job_role || "",
        date_of_joining: editingEmployee.date_of_joining || "",
        projects: editingEmployee.projects || [],
        profile_image: null,
      });

      setImagePreview(editingEmployee.profile_image || "");
    } else {
      setForm(initialForm);
      setImagePreview("");
    }

    setMessage("");
    setError("");
    setImageError("");
  }, [editingEmployee]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((previous) => ({ ...previous, [name]: value }));
  };

  const handleProjects = (e) => {
    const selected = Array.from(
      e.target.selectedOptions,
      (option) => Number(option.value)
    );

    setForm((previous) => ({ ...previous, projects: selected }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files?.[0];

    setImageError("");

    if (!file) return;

    const allowedTypes = ["image/jpeg", "image/png", "image/webp"];

    if (!allowedTypes.includes(file.type)) {
      setImageError("Only JPEG, PNG and WebP images are allowed.");
      e.target.value = "";
      return;
    }

    if (file.size > 2 * 1024 * 1024) {
      setImageError("Image size must not exceed 2 MB.");
      e.target.value = "";
      return;
    }

    setForm((previous) => ({ ...previous, profile_image: file }));
    setImagePreview(URL.createObjectURL(file));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    setError("");

    try {
      const data = {
        ...form,
        department: Number(form.department),
        salary: Number(form.salary),
      };

      if (editingEmployee) {
        await updateEmployee(editingEmployee.id, data);
        setMessage("Employee updated successfully!");
      } else {
        await createEmployee(data);
        setMessage("Employee added successfully!");
      }

      onSaved();
      setForm(initialForm);
      setImagePreview("");
    } catch (err) {
      const responseData = err.response?.data;

      setError(
        responseData && typeof responseData === "object"
          ? Object.entries(responseData)
              .map(([field, messages]) =>
                `${field}: ${Array.isArray(messages) ? messages.join(", ") : messages}`
              )
              .join(" | ")
          : "Unable to save employee. Please check your details."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h4 className="fw-bold mb-3">
        {editingEmployee ? "Edit Employee" : "Add New Employee"}
      </h4>

      {message && <div className="alert alert-success">{message}</div>}
      {error && <div className="alert alert-danger">{error}</div>}

      {optionsLoading ? (
        <div className="text-center py-3">
          <div className="spinner-border text-primary" role="status" />
          <p className="mt-2">Loading form options...</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <div className="row g-3">

            <div className="col-12">
              <label className="form-label">Employee Profile Image</label>
              <input
                className="form-control"
                type="file"
                accept="image/jpeg,image/png,image/webp"
                onChange={handleImageChange}
              />
              <small className="text-muted">
                JPEG, PNG or WebP. Maximum size: 2 MB.
              </small>

              {imageError && (
                <div className="text-danger small mt-2">{imageError}</div>
              )}

              {imagePreview && (
                <div className="mt-3">
                  <img
                    src={imagePreview}
                    alt="Employee profile preview"
                    style={{
                      width: "120px",
                      height: "120px",
                      objectFit: "cover",
                      borderRadius: "50%",
                    }}
                  />
                </div>
              )}
            </div>

            <div className="col-12 col-md-6">
              <label className="form-label">Employee ID</label>
              <input className="form-control" name="employee_id"
                value={form.employee_id} onChange={handleChange} required />
            </div>

            <div className="col-12 col-md-6">
              <label className="form-label">Employee Name</label>
              <input className="form-control" name="name"
                value={form.name} onChange={handleChange} required />
            </div>

            <div className="col-12 col-md-6">
              <label className="form-label">Email</label>
              <input className="form-control" type="email" name="email"
                value={form.email} onChange={handleChange} required />
            </div>

            <div className="col-12 col-md-6">
              <label className="form-label">Phone Number</label>
              <input className="form-control" type="tel" name="phone"
                value={form.phone} onChange={handleChange}
                pattern="[0-9]{10}" maxLength="10" required />
            </div>

            <div className="col-12 col-md-6">
              <label className="form-label">Salary</label>
              <input className="form-control" type="number" name="salary"
                value={form.salary} onChange={handleChange}
                min="0.01" step="0.01" required />
            </div>

            <div className="col-12 col-md-6">
              <label className="form-label">Department</label>
              <select className="form-select" name="department"
                value={form.department} onChange={handleChange} required>
                <option value="">Select Department</option>
                {departments.map((department) => (
                  <option key={department.id} value={department.id}>
                    {department.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="col-12 col-md-6">
              <label className="form-label">Job Role</label>
              <input className="form-control" name="job_role"
                value={form.job_role} onChange={handleChange} required />
            </div>

            <div className="col-12 col-md-6">
              <label className="form-label">Date of Joining</label>
              <input className="form-control" type="date"
                name="date_of_joining" value={form.date_of_joining}
                onChange={handleChange} required />
            </div>

            <div className="col-12">
              <label className="form-label">Projects</label>
              <select className="form-select" multiple size="4"
                value={form.projects.map(String)} onChange={handleProjects}>
                {projects.map((project) => (
                  <option key={project.id} value={project.id}>
                    {project.name}
                  </option>
                ))}
              </select>
              <small className="text-muted">
                Hold Ctrl (or Command on Mac) to select multiple projects.
              </small>
            </div>

            <div className="col-12 d-flex flex-wrap gap-2">
              <button type="submit" className="btn btn-primary"
                disabled={loading || optionsLoading}>
                {loading ? "Saving..." :
                  editingEmployee ? "Update Employee" : "Add Employee"}
              </button>

              {editingEmployee && (
                <button type="button" className="btn btn-secondary"
                  onClick={onCancel} disabled={loading}>
                  Cancel
                </button>
              )}
            </div>
          </div>
        </form>
      )}
    </div>
  );
}

export default EmployeeForm;
