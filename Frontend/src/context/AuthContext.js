import React, { createContext, useContext, useEffect, useState } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [role, setRole] = useState(() => {
        // Intenta cargar el role desde localStorage
        return localStorage.getItem('role') || null;
    });

    // Este efecto se ejecuta cuando el role cambia
    useEffect(() => {
        if (role) {
            localStorage.setItem('role', role); // Guardar el role en localStorage
        } else {
            localStorage.removeItem('role'); // Eliminar el role de localStorage si no está autenticado
        }
    }, [role]);

    return (
        <AuthContext.Provider value={{ role, setRole }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
