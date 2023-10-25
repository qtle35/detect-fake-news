import { Navigate } from 'react-router-dom'
import { useAuth } from './auth-context'

function PrivateRoute({ children }) {
    const { userIsAuthenticated } = useAuth()
    return userIsAuthenticated() ? children : <Navigate to="/login" />
}

export default PrivateRoute