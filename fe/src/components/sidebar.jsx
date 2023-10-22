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

function CustomSidebar() {
    const [collapsed, setCollapsed] = useState(false);
    const collapseSidebar = () => {
        setCollapsed(!collapsed);
    };
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
                <MenuItem icon={<FaHome />} component={<Link to="/home" />}>Home</MenuItem>
                <MenuItem icon={<FaHeart />}>Team</MenuItem>
                <MenuItem icon={<FaAngleDoubleRight />}>Contacts</MenuItem>
                <MenuItem icon={<FaTachometerAlt />}>Profile</MenuItem>
                <MenuItem icon={<FaGem />}>FAQ</MenuItem>
                <MenuItem icon={<FaRegLaughWink />}>Calendar</MenuItem>
            </Menu>
        </Sidebar>

    );
};

export default CustomSidebar;