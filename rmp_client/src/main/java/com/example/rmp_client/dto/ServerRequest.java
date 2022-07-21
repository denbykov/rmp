package com.example.rmp_client.dto;

public class ServerRequest {

    String url;
    RequestMethod method;
    String jsonPayload;

    public RequestMethod getMethod() {
        return method;
    }

    public String getJsonPayload() {
        return jsonPayload;
    }

    public String getUrl() {
        return url;
    }

    public void setJsonPayload(String jsonPayload) {
        this.jsonPayload = jsonPayload;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    @Override
    public String toString() {
        return "ServerRequest{" +
                "url='" + url + '\'' +
                ", method=" + method +
                ", jsonPayload='" + jsonPayload + '\'' +
                '}';
    }
}
