/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package greenhouseoptws;

/**
 *
 * @author Roxana
 */
public class Request {
    private double opt_temp;
    private double budget;

    public Request() {
    }

    public Request(double opt_temp, double budget) {
        this.opt_temp = opt_temp;
        this.budget = budget;
    }

    public double getOpt_temp() {
        return opt_temp;
    }

    public void setOpt_temp(double opt_temp) {
        this.opt_temp = opt_temp;
    }

    public double getBudget() {
        return budget;
    }

    public void setBudget(double budget) {
        this.budget = budget;
    }
    
    
    
}
