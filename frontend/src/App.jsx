import { Routes, Route, Navigate } from "react-router-dom";

import { AuthProvider, useAuth } from "./context/AuthContext";

import Login from "./components/Login";
import Navbar from "./components/layout/Navbar";
import ProtectedRoute from "./routes/ProtectedRoute";

import AdminDashboard from "./pages/AdminDashboard";
import EmployeeDashboard from "./pages/EmployeeDashboard";

function Unauthorized() {
  return (
    <div className="container py-5 text-center">
      <h2 className="text-danger">403 - Access Denied</h2>
      <p>You don't have permission to access this page.</p>
    </div>
  );
}

function AppRoutes() {
  const { isAuthenticated, role } = useAuth();

  const home = isAuthenticated
    ? role === "Admin"
      ? "/admin-dashboard"
      : role === "Employee"
        ? "/employee-dashboard"
        : "/unauthorized"
    : "/login";

  return (
    <>
      {isAuthenticated && <Navbar />}

      <Routes>
        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedRoute allowedRoles={["Admin"]} />}>
          <Route path="/admin-dashboard" element={<AdminDashboard />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={["Employee"]} />}>
          <Route path="/employee-dashboard" element={<EmployeeDashboard />} />
        </Route>

        <Route path="/unauthorized" element={<Unauthorized />} />

        <Route path="/" element={<Navigate to={home} replace />} />

        <Route path="*" element={<Navigate to={home} replace />} />
      </Routes>
    </>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}

export default App;