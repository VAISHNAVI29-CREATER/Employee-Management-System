import { useEffect, useState } from "react";
import { getEmployees } from "../services/employeeService";

function EmployeeDashboard() {
  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchEmployee = async () => {
      try {
        const data = await getEmployees();
        const records = data.results || data;
        setEmployee(records[0] || null);
      } catch (err) {
        setError("Unable to load employee details.");
      } finally {
        setLoading(false);
      }
    };

    fetchEmployee();
  }, []);

  if (loading) {
    return <div className="container py-5">Loading your details...</div>;
  }

  if (error) {
    return <div className="container py-5 alert alert-danger">{error}</div>;
  }

  if (!employee) {
    return <div className="container py-5">No employee profile found.</div>;
  }

  const details = [
    ["Employee ID", employee.employee_id],
    ["Name", employee.name],
    ["Email", employee.email],
    ["Phone", employee.phone],
    ["Department", employee.department_name],
    ["Job Role", employee.job_role],
    ["Salary", employee.salary],
    ["Date of Joining", employee.date_of_joining],
    ["Projects", employee.project_names?.join(", ") || "None"],
  ];

  return (
    <div className="container py-4">
      <div className="mb-4">
        <h2 className="fw-bold">Employee Dashboard</h2>
        <p className="text-muted">View your employee information.</p>
      </div>

      <div className="card shadow-sm border-0">
        <div className="card-header bg-primary text-white py-3">
          <h5 className="mb-0">My Profile</h5>
        </div>

        <div className="card-body">
          <div className="row">
            {details.map(([label, value]) => (
              <div className="col-md-6 mb-4" key={label}>
                <small className="text-muted">{label}</small>
                <div className="fw-semibold">{value || "Not available"}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default EmployeeDashboard;