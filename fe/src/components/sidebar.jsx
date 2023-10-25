import { Link, NavLink } from 'react-router-dom';
import { Sidebar, Menu, MenuItem } from 'react-pro-sidebar';
import { useState } from 'react';
import {
    FaUser,
    FaAngleDoubleLeft,
    FaAngleDoubleRight,
    FaTachometerAlt,
    FaGem,
    FaList,
    FaRegLaughWink,
    FaHeart,
    FaHome
} from 'react-icons/fa';
import { useAuth } from './auth-context';

function CustomSidebar() {
    const { userIsAuthenticated, userLogout } = useAuth()
    const [collapsed, setCollapsed] = useState(false);
    const collapseSidebar = () => {
        setCollapsed(!collapsed);
    };
    const logout = async (event) => {
        event.preventDefault();
        await userLogout()
        window.location.href = '/login'
    }
    return (
        <Sidebar style={{ height: "100%" }} collapsed={collapsed}>
            <Menu>
                <MenuItem
                    icon={<FaList />}
                    onClick={collapseSidebar}
                    style={{ textAlign: "center" }}
                >
                    <h2>Admin</h2>
                </MenuItem>
                <MenuItem icon={<FaHome />} component={<Link to="/" />}>Home</MenuItem>
                <MenuItem icon={<FaHeart />}>Team</MenuItem>
                <MenuItem icon={<FaAngleDoubleRight />}>Contacts</MenuItem>
                <MenuItem icon={<FaTachometerAlt />} component={<Link to="/label" />}>Label</MenuItem>
                {!userIsAuthenticated() && <MenuItem icon={<FaGem />} component={<Link to="/login" />}>Login</MenuItem>}
                {userIsAuthenticated() && <p>Admin</p>}
                {userIsAuthenticated() && <MenuItem icon={<FaRegLaughWink />} onClick={logout}>Logout</MenuItem>}
            </Menu>
        </Sidebar>

    );
};

export default CustomSidebar;