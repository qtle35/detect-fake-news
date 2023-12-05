package com.httm;

import java.util.Collections;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class HttmApplication {

	public static void main(String[] args) {
		SpringApplication app = new SpringApplication(HttmApplication.class);
		app.setDefaultProperties(Collections.singletonMap("server.port", "5000"));
		app.run(args);
	}

}
