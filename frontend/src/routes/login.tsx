import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import instance from "@/api/API";

export default function Login() {
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState("");

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCredentials((prevCredentials) => ({
      ...prevCredentials,
      [name]: value,
    }));
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      // Make a POST request to your login endpoint
      const response = await instance.post("/login", credentials);

      // Assuming your API returns a token upon successful login
      const token = response.data.access_token;

      // You can store the token in localStorage or a state management solution
      // For example, you might use Redux or React Context for global state management
      localStorage.setItem("token", token);

      // Redirect to the desired page upon successful login
      navigate("/dashboard");
    } catch (error) {
      // Handle login error, show a message to the user, etc.
      console.error("Login failed", error);
      setError("Invalid username or password");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-800">
      <div className="w-full max-w-md mx-auto p-6 space-y-6 border rounded-lg shadow-lg bg-white dark:bg-gray-900">
        <h1 className="text-3xl font-bold text-center">Login</h1>
        <form className="space-y-6" onSubmit={handleLogin}>
          <div className="space-y-2">
            <label htmlFor="username">Username</label>
            <input
              className="w-full px-3 py-2 border rounded-lg"
              id="username"
              name="username"
              placeholder="Enter your username"
              required
              type="text"
              value={credentials.username}
              onChange={handleInputChange}
            />
          </div>
          <div className="space-y-2">
            <label htmlFor="password">Password</label>
            <input
              className="w-full px-3 py-2 border rounded-lg"
              id="password"
              name="password"
              placeholder="Enter your password"
              required
              type="password"
              value={credentials.password}
              onChange={handleInputChange}
            />
          </div>
          {error && <p className="text-red-500">{error}</p>}
          <div>
            <button
              className="w-full px-4 py-2 font-bold text-white bg-blue-500 rounded-lg hover:bg-blue-700"
              type="submit"
            >
              Login
            </button>
          </div>
        </form>
        <div className="flex justify-center items-center">
          <p className="text-gray-600">
            Don't have an account?{" "}
            <a
              className="text-blue-500 cursor-pointer"
              onClick={() => navigate("/signup")}
            >
              Create Account
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
