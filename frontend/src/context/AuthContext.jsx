import { createContext, useContext, useState } from "react";
import api from "../api/axios";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(
    () => localStorage.getItem("authToken")
  );

  const [user, setUser] = useState(
    () => JSON.parse(localStorage.getItem("authUser") || "null")
  );

  const login = async (username, password) => {
    const response = await api.post("auth/token/", {
      username,
      password,
    });

    const newToken = response.data.token;

    const userResponse = await api.get("auth/user/", {
      headers: {
        Authorization: `Token ${newToken}`,
      },
    });

    const userData = userResponse.data;

    localStorage.setItem("authToken", newToken);
    localStorage.setItem("authUser", JSON.stringify(userData));

    setToken(newToken);
    setUser(userData);

    return userData;
  };

  const logout = () => {
    localStorage.removeItem("authToken");
    localStorage.removeItem("authUser");

    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        role: user?.role,
        isAuthenticated: Boolean(token && user),
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}