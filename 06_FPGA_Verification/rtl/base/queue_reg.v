
module queue_reg #(
    parameter width = 8, 
    parameter depth = 3
    )(
    input wire clk,
    input wire rst,
    input wire ce,
    input wire input_vld,
    input wire read_flag,
    input wire [width-1:0] din,
    output reg [width-1:0] dout
);

    // block ram
    // 改为时序逻辑电路，读信号进来后需等一个时钟周期才能输出正确的数据
    reg [width*depth-1:0] qr;
    reg [31:0] raddr;

    // assign dout = (read_flag==1'b1)? qr[width*raddr-1 -: width]:dout;   // vivado simulation
    // // assign dout = (read_flag==1'b1)? qr[width*(raddr+1)-1 -: width]:dout;    // quata simulation


    always@(posedge clk) begin
        if(rst == 1'b0) begin
            dout <= 0;
        end else begin
            if(read_flag == 1'b1) begin
                dout <= qr[width*raddr-1 -: width];
            end else begin
                dout <= dout;
            end
        end
    end

    always@(posedge clk) begin
        if(rst == 1'b0) begin
            qr <= 0;
        end else if(input_vld) begin
            // qr <= qr << width;
            // qr[width-1:0] <= din;
            qr <= {qr[width*(depth-1)-1:0], din};
        end else begin
            qr <= qr;
        end
    end

    always@(posedge clk) begin
        if(rst == 1'b0) begin
            raddr <= 0;
        end else begin
            if(input_vld == 1'b1 && read_flag == 1'b1) begin
                raddr <= raddr;
            end else if(input_vld == 1'b1) begin
                raddr <= raddr+1;
            end else if(read_flag == 1'b1) begin
                raddr <= raddr-1;
            end else begin
                raddr <= raddr;
            end
        end
    end

    // // Dump waves
    // initial begin
    //     $dumpfile("queue_reg.vcd");
    //     $dumpvars(1, queue_reg);
    // end

endmodule