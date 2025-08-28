import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface User {
    id: string;
    email: string;
    first_name: string;
    last_name: string;
    is_active: boolean;
    full_name: string;
}

export interface AuthState {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    error: string | null;
}

export interface AuthActions {
    login: (email: string, password: string) => Promise<void>;
    register: (email: string, password: string, firstName: string, lastName: string) => Promise<void>;
    logout: () => void;
    clearError: () => void;
    setLoading: (loading: boolean) => void;
    setError: (error: string) => void;
}

export type AuthStore = AuthState & AuthActions;

const initialState: AuthState = {
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,
};

export const useAuthStore = create<AuthStore>()(
    persist(
        (set, get) => ({
            ...initialState,

            login: async (email: string, password: string) => {
                set({ isLoading: true, error: null });

                try {
                    const formData = new FormData();
                    formData.append('username', email);
                    formData.append('password', password);

                    const response = await fetch('http://localhost:8000/auth/login', {
                        method: 'POST',
                        body: formData,
                    });

                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'Login failed');
                    }

                    const data = await response.json();

                    // Get user info
                    const userResponse = await fetch('http://localhost:8000/auth/me', {
                        headers: {
                            'Authorization': `Bearer ${data.access_token}`,
                        },
                    });

                    if (!userResponse.ok) {
                        throw new Error('Failed to get user info');
                    }

                    const userData = await userResponse.json();

                    set({
                        user: userData,
                        token: data.access_token,
                        isAuthenticated: true,
                        isLoading: false,
                        error: null,
                    });
                } catch (error) {
                    set({
                        isLoading: false,
                        error: error instanceof Error ? error.message : 'Login failed',
                    });
                    throw error;
                }
            },

            register: async (email: string, password: string, firstName: string, lastName: string) => {
                set({ isLoading: true, error: null });

                try {
                    const response = await fetch('http://localhost:8000/auth/register', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            email,
                            password,
                            first_name: firstName,
                            last_name: lastName,
                        }),
                    });

                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'Registration failed');
                    }

                    const userData = await response.json();

                    set({
                        isLoading: false,
                        error: null,
                    });

                    // Return user data so the component can handle navigation
                    return userData;
                } catch (error) {
                    set({
                        isLoading: false,
                        error: error instanceof Error ? error.message : 'Registration failed',
                    });
                    throw error;
                }
            },

            logout: () => {
                set({
                    user: null,
                    token: null,
                    isAuthenticated: false,
                    error: null,
                });
            },

            clearError: () => {
                set({ error: null });
            },

            setLoading: (loading: boolean) => {
                set({ isLoading: loading });
            },

            setError: (error: string) => {
                set({ error });
            },
        }),
        {
            name: 'auth-storage',
            partialize: (state) => ({
                user: state.user,
                token: state.token,
                isAuthenticated: state.isAuthenticated,
            }),
        }
    )
);
