package client.views;


import client.entities.UserCredentials;
import javafx.fxml.FXML;
import javafx.scene.control.TextField;

public class RegistrationView {

    @FXML
    private TextField name;

    @FXML
    private TextField password;

    @FXML
    protected void UserInformation() {
        System.out.println(name.getText());
        System.out.println(password.getText());
    }


    public UserCredentials formCredentials() {
        return null;
    }

    public void setError(String error) {

    }
    public void draw(){

    }
}
