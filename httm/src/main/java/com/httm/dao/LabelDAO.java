package com.httm.dao;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;

import com.httm.model.Label;

public class LabelDAO extends DAO {
	public LabelDAO() {
		super();
	}

	public ArrayList<Label> getLabel(String key) {
        String sql ="""
					SELECT * FROM label
					WHERE name LIKE ?;
					""";
        try{
            PreparedStatement ps = con.prepareStatement(sql);
            ps.setString(1, "%"+key+"%");
            ResultSet rs = ps.executeQuery();
            ArrayList<Label> listLabel = new ArrayList<>();
            while (rs.next()){
            	Label l = new Label();
                l.setId(rs.getInt("id"));
                l.setName(rs.getString("name"));
                l.setDescription(rs.getString("description"));
                listLabel.add(l);
            }
            return listLabel;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
	public Label getOneLabel(int id) {
        String sql ="""
					SELECT * FROM label
					WHERE id = ?;
					""";
        try{
            PreparedStatement ps = con.prepareStatement(sql);
            ps.setInt(1, id);
            ResultSet rs = ps.executeQuery();
            Label label = new Label();
            if (rs.next()){
            	label.setId(rs.getInt("id"));
            	label.setName(rs.getString("name"));
            	label.setDescription(rs.getString("description"));
            }
            return label;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
	public boolean saveLabel(Label label) {
		boolean kq = false;
		String sql ="""
				INSERT INTO label(name, description) VALUES
				(?, ?);
				""";
	    try{
	    	this.con.setAutoCommit(false);
	        PreparedStatement ps = con.prepareStatement(sql);
	        ps.setString(1, label.getName());
	        ps.setString(2, label.getDescription());
	        ps.executeUpdate();
	        this.con.commit();
	        kq = true;
	    } catch (Exception e) {
	    	try {
                this.con.rollback();
            } catch (Exception ex){
            	ex.printStackTrace();
            }
			kq = false;
			e.printStackTrace();
	    } finally{
            try {
                this.con.setAutoCommit(true);
            } catch (Exception ex){
            	kq = false;
                ex.printStackTrace();
            }
        }
		return kq;
	}
	
	public boolean updateLabel(Label label) {
		boolean kq = false;
		String sql ="""
					UPDATE label
					SET name = ?, description = ?
					WHERE id = ?;
					""";
		try{
			this.con.setAutoCommit(false);
			PreparedStatement ps = con.prepareStatement(sql);
			ps.setString(1, label.getName());
			ps.setString(2, label.getDescription());
			ps.setInt(3, label.getId());
			ps.executeUpdate();
			this.con.commit();
			kq = true;
		} catch (Exception e) {
			try {
                this.con.rollback();
            } catch (Exception ex){
            	ex.printStackTrace();
            }
			kq = false;
			e.printStackTrace();
		} finally{
            try {
                this.con.setAutoCommit(true);
            } catch (Exception ex){
            	kq = false;
                ex.printStackTrace();
            }
        }
		return kq;
	}
	
	public boolean deleteLabel(int id) {
		boolean kq = false;
		String sql ="""
					DELETE FROM label
					WHERE id = ?;
					""";
		try{
			this.con.setAutoCommit(false);
			PreparedStatement ps = con.prepareStatement(sql);
			ps.setInt(1, id);
			ps.executeUpdate();
			this.con.commit();
			kq = true;
		} catch (Exception e) {
			try {
                this.con.rollback();
            } catch (Exception ex){
            	ex.printStackTrace();
            }
			kq = false;
			e.printStackTrace();
		} finally{
            try {
                this.con.setAutoCommit(true);
            } catch (Exception ex){
            	kq = false;
                ex.printStackTrace();
            }
        }
		return kq;
	}
	
}
