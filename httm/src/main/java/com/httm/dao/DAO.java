package com.httm.dao;

import java.sql.*;

public class DAO {
	public Connection con;
	public DAO(){
        if(con == null){
            String dbUrl = "jdbc:mysql://localhost:3306/flask_data";
            String dbClass = "com.mysql.cj.jdbc.Driver";
 
            try {
                Class.forName(dbClass);
                con = DriverManager.getConnection (dbUrl, "root", "a123456");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
