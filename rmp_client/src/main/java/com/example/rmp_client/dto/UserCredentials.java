package com.example.rmp_client.dto;



public class UserCredentials {
    String name;
    String password;

    public String getName() {
        return name;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "ServerResponse{" +
                "name='" + name + '\'' +
                ", password='" + password + '\'' +
                '}';
    }

}
