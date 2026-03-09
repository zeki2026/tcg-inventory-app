import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';

interface User {
    email: string;
}

interface AuthContextType {
    user: User | null;
    login: (token: string) => void;
    logout: () => void;
    isAuthenticated: boolean;
    loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    // We need useNavigate here but AuthProvider is inside Router usually. 
    // Ideally AuthProvider should be inside Router in App.tsx.

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            // Validate token or just assume valid for now and fetch user profile if exists
            // For now, we'll just set a dummy user or decode token if needed.
            // Better: fetch /users/me
            // But we don't have that endpoint yet implemented fully and verified.
            // Let's assume valid if token exists for MVP.
            setUser({ email: 'user@example.com' }); // Placeholder
        }
        setLoading(false);
    }, []);

    const login = (token: string) => {
        localStorage.setItem('token', token);
        setUser({ email: 'user@example.com' });
        // Navigation should happen in the component calling login
    };

    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
