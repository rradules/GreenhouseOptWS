/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package beans;

/**
 *
 * @author Roxana
 */
public class Request {
    //wT, wB, T_opt, B_opt, budget, max_T_heat, max_B_light

    private double opt_temp;
    private double budget;
    private double max_temp_heat;
    private double wT;
    private double wB;
    private double opt_bright;
    private double max_bright_light;

    public Request() {
    }

    public double getMax_temp_heat() {
        return max_temp_heat;
    }

    public void setMax_temp_heat(double max_temp_heat) {
        this.max_temp_heat = max_temp_heat;
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

    public double getwT() {
        return wT;
    }

    public void setwT(double wT) {
        this.wT = wT;
    }

    public double getwB() {
        return wB;
    }

    public void setwB(double wB) {
        this.wB = wB;
    }

    public double getOpt_bright() {
        return opt_bright;
    }

    public void setOpt_bright(double opt_bright) {
        this.opt_bright = opt_bright;
    }

    public double getMax_bright_light() {
        return max_bright_light;
    }

    public void setMax_bright_light(double max_bright_light) {
        this.max_bright_light = max_bright_light;
    }
}
