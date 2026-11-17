import api from "../api/axios";

export const loginUser = async (username, password) => {
  const response = await api.post("auth/token/", {
    username,
    password,
  });

  localStorage.setItem("authToken", response.data.token);

  return response.data;
};

export const logoutUser = () => {
  localStorage.removeItem("authToken");
};