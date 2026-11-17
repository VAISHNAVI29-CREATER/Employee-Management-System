
import api from "../api/axios";

// Convert employee data into FormData
const createFormData = (employeeData) => {
  const formData = new FormData();

  Object.entries(employeeData).forEach(([key, value]) => {
    if (value === null || value === undefined) return;

    if (key === "profile_image" && !(value instanceof File)) {
      return;
    }

    if (key === "projects" && Array.isArray(value)) {
      value.forEach((projectId) => {
        formData.append("projects", projectId);
      });
      return;
    }

    formData.append(key, value);
  });

  return formData;
};

// Get all employees
export const getEmployees = async () => {
  const response = await api.get("employees/");
  return response.data;
};

// Create an employee
export const createEmployee = async (employeeData) => {
  const formData = createFormData(employeeData);

  const response = await api.post("employees/", formData);
  return response.data;
};

// Update an employee
export const updateEmployee = async (id, employeeData) => {
  const formData = createFormData(employeeData);

  const response = await api.patch(
    `employees/${id}/`,
    formData
  );
  return response.data;
};

// Delete an employee
export const deleteEmployee = async (id) => {
  const response = await api.delete(`employees/${id}/`);
  return response.data;
};

// Get departments
export const getDepartments = async () => {
  const response = await api.get("departments/");
  return response.data;
};

// Get projects
export const getProjects = async () => {
  const response = await api.get("projects/");
  return response.data;
};
