package com.httm.controller;

import java.util.ArrayList;

import org.springframework.web.bind.annotation.*;

import com.httm.dao.LabelDAO;
import com.httm.model.Label;

@RestController
@RequestMapping("/label")
@CrossOrigin
public class LabelController {
	public final LabelDAO dao;
	public LabelController() {
		this.dao = new LabelDAO();
	}
	
	@GetMapping()
	public ArrayList<Label> getAllLabels(@RequestParam(required = false, defaultValue = "") String key) {
		return dao.getLabel(key);
	}
	
	@GetMapping("/{id}")
	public Label getOneLabel(@PathVariable int id) {
		return dao.getOneLabel(id);
	}
	
	@PostMapping("/new")
	public boolean createLabel(@RequestBody Label label) {
		return dao.saveLabel(label);
	}

	@PutMapping()
	public boolean updateLabel(@RequestBody Label label) {
		return dao.updateLabel(label);
	}
	
	@DeleteMapping("/{id}")
	public boolean deleteLabel(@PathVariable int id) {
		return dao.deleteLabel(id);
	}
}
