import {
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    RESET_PASSWORD_SUCCESS,
    RESET_PASSWORD_FAIL,
    RESET_PASSWORD_CONFIRM_SUCCESS,
    RESET_PASSWORD_CONFIRM_FAIL,
    SET_AUTH_LOADING,
    REMOVE_AUTH_LOADING,
    AUTHENTICATED_FAIL,
    AUTHENTICATED_SUCCESS,
    REFRESH_SUCCESS,
    REFRESH_FAIL,
    LOGOUT,
    USER_LOADED_SUCCESS,
    USER_LOADED_FAIL
} from '../actions/login/types'
import { useActionData } from 'react-router-dom';
import { refresh } from 'redux/actions/login/auth';

const initialState = {
    access: localStorage.getItem('access'),
    refresh: localStorage.getItem('refresh'),
    isAuthenticated: null,
    user: null,
    loading: false,
    user_loading: true,
}

export default function auth(state = initialState, action){
    const {type, payload} = action;

    switch(type) {
        case USER_LOADED_SUCCESS:
            return {
                ...state,
                user: payload,
                user_loading: false
            }
        case USER_LOADED_FAIL:
            return {
                ...state,
                user: null,
                user_loading: false
            }
        case SET_AUTH_LOADING:
            return {
                ...state,
                loading: true
            }
        case REMOVE_AUTH_LOADING:
            return {
                ...state,
                loading: false
            }
        case AUTHENTICATED_SUCCESS:
            return {
                ...state,
                isAuthenticated: true
            }
        case AUTHENTICATED_FAIL:
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            return {
                ...state,
                isAuthenticated: false,
                access: null,
                refresh: null    
            }
        case LOGIN_SUCCESS:
            localStorage.setItem('access', payload.access);
            localStorage.setItem('refresh', payload.refresh);
            return {
                ...state,
                isAuthenticated: true,
                access: localStorage.getItem('access'),
                refresh: localStorage.getItem('refresh')
            }
        case RESET_PASSWORD_SUCCESS:
        case RESET_PASSWORD_FAIL:
        case RESET_PASSWORD_CONFIRM_SUCCESS:
        case RESET_PASSWORD_CONFIRM_FAIL:
            return {
                ...state
            }
        
        case REFRESH_SUCCESS:
            localStorage.setItem('access', payload.access)
            return {
                ...state
            }
        case LOGIN_FAIL:
        case REFRESH_FAIL:
        case LOGOUT:
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            return {
                ...state,
                access: null,
                refresh: null,
                isAuthenticated: false,
                user: null
            }
        default:
            return state
    }
} 