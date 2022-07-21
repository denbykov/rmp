package client.entities;

public enum ResponseCode {

    INFORMATIONAL(100),
    SUCCESS(200),
    REDIRECTION(300),
    CLIENT_ERROR(400),
    SERVER_ERROR(500);

    private Integer code;

    ResponseCode(Integer code) {
        this.code = code;
    }

    public Integer getMethod() {
        return code;
    }
}
