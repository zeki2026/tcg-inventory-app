import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { LogOut, LayoutDashboard, CreditCard, Activity } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Dashboard = () => {
    const { logout, user } = useAuth();
    const navigate = useNavigate();
    const [stats, setStats] = useState<any>(null);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await api.get('/dashboard/stats');
                setStats(response.data);
            } catch (error) {
                console.error('Error fetching stats', error);
            }
        };
        fetchStats();
    }, []);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="dashboard-container">
            <aside className="sidebar">
                <div className="sidebar-header">
                    <h2>TCG Manager</h2>
                </div>
                <nav>
                    <a className="active"><LayoutDashboard size={20} /> Dashboard</a>
                    <a><CreditCard size={20} /> Inventory</a>
                    <a><Activity size={20} /> Reports</a>
                </nav>
                <div className="sidebar-footer">
                    <button onClick={handleLogout} className="logout-btn">
                        <LogOut size={18} /> Logout
                    </button>
                </div>
            </aside>

            <main className="main-content">
                <header>
                    <h1>Dashboard</h1>
                    <div className="user-profile">
                        <span>{user?.email}</span>
                        <div className="avatar">U</div>
                    </div>
                </header>

                <div className="stats-grid">
                    <div className="stat-card">
                        <h3>Total Cards</h3>
                        <p className="stat-value">{stats?.total_cards || 0}</p>
                    </div>
                    <div className="stat-card">
                        <h3>Total Value</h3>
                        <p className="stat-value">${stats?.total_value || 0}</p>
                    </div>
                </div>
            </main>
        </div>
    );
};
