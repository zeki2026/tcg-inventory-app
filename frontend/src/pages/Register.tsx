import { KeyRound, Lock, User } from "lucide-react";
import React, { useEffect, useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";


export const Register = () => {
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    useEffect( () =>{
            console.log(error);
        }, [error])
    const handleSubmit = async (e: React.FormEvent) =>{
        e.preventDefault();
        try{
            const userData = {
            email: username, // Asegúrate de que los nombres coincidan con UserCreate
            password: password  // O el rol que corresponda según tu UserCreate
        };
            const response = await api.post('/api/v1/auth/register',userData );
            console.log(response)
        }catch(err :any ){
            // 1. Error de respuesta del servidor (400, 401, 422, 500)
            if (err.response) {
                const serverMessage = err.response.data?.detail;
                
                // Si es un error 422 de validación, 'detail' es un array
                if (Array.isArray(serverMessage)) {
                    setError(`Error de validación: ${serverMessage[0].msg}`);
                } else {
                    // Si es un error 400/401, 'detail' suele ser un string
                    setError(serverMessage || 'Credenciales inválidas');
                }
                
                console.error("Detalle del servidor:", err.response.data);
            } 
            // 2. El servidor no respondió (Error de red/Docker abajo)
            else if (err.request) {
                setError('No se pudo conectar con el servidor. Verifica tu conexión.');
                console.error("Error de red:", err.request);
            } 
            // 3. Error al configurar la petición
            else {
                setError('Ocurrió un error inesperado.');
                console.error("Error:", err.message);
            } 
        }
    };

    const login = () =>{
        navigate('/login')
    }

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <div className="icon-bg">
                        <KeyRound size={32} color="white" />
                    </div>
                    <h1>Welcome, please Register your User</h1>
                    <p>Register to manage your inventory</p>
                </div>

                <form onSubmit={handleSubmit} className="login-form">
                    <div className="form-group">
                        <label>Username</label>
                        <div className="input-wrapper">
                            <User size={20} className="input-icon" />
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="Enter your username"
                                required
                            />
                        </div>
                    </div>

                    <div className="form-group">
                        <label>Password</label>
                        <div className="input-wrapper">
                            <Lock size={20} className="input-icon" />
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Enter your password"
                                required
                            />
                        </div>
                    </div>

                    {error && <div className="error-message">{error}</div>}

                    <button type="submit" className="login-btn">
                        Register
                    </button>
                </form>

                <div className='register-container'>
                    <button onClick={login}  className="btn">Sign in</button>
                </div>
            </div>
        </div>
    );

};