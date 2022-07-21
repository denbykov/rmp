package com.example.rmp_client.dto;

public enum RequestMethod {

    GET("GET"),
    POST("POST"),
    PUT("PUT");

    private String method;

    RequestMethod(String method) {
        this.method = method;
    }

    public String getMethod() {
        return method;
    }
}
