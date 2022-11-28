// 由于结构的设计，被加树数先进来，乘数后进来

module mac_unit #(
    parameter N = 32
    )(
    input wire clk,
    input wire rst_n,
    input wire ce,
    input wire multiplicand_vld,
    input wire addend_vld,
    input wire [N-1:0] multiplicand_din,
    input wire [N-1:0] multiplier_din,
    input wire [31:0] addend_din,
    output reg [31:0] mac_dout,
    output reg mac_dout_vld
);
    reg addend_temp_vld;
    reg [31:0] addend_temp;
    reg multiplicand_temp_vld;
    reg [N-1:0] multiplicand_temp;

    wire [31:0] product;
    wire product_dout_vld;
    wire product_end;

    qmult #(.N(N)) u_mult(
        .clk(clk),
        .rst_n(rst_n),
        .ce(ce),
        .input_vld(addend_temp_vld & multiplicand_temp_vld),
        .multiplicand_din(multiplicand_temp),
        .multiplier_din(multiplier_din),
        .product_dout(product),
        .product_dout_vld(product_dout_vld),
        .product_end(product_end)
    );

    // 加数有效位锁存，如果乘数来了就释放加数有效位
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            addend_temp_vld <= 1'b0;
        end else begin
            if(addend_vld) begin
                addend_temp_vld <= 1'b1;
            end else if(multiplicand_temp_vld) begin
                addend_temp_vld <= 1'b0;
            end else begin
                addend_temp_vld <= addend_temp_vld;
            end
        end
    end

    // 加数锁存
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            addend_temp <= 0;
        end else begin
            if(addend_vld == 1'b1) begin
                addend_temp <= addend_din;
            end else begin
                addend_temp <= addend_temp;
            end
        end
    end

    // 乘数有效位打一拍，加数有效位因为锁存后慢一拍，如果乘数不慢一拍，两者同时来有效位不能同时为1
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            multiplicand_temp_vld <= 1'b0;
        end else begin
            multiplicand_temp_vld <= multiplicand_vld;
        end
    end

    // 乘数锁存
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            multiplicand_temp <= 0;
        end else begin
            if(multiplicand_vld == 1'b1) begin
                multiplicand_temp <= multiplicand_din;
            end else begin
                multiplicand_temp <= multiplicand_temp;
            end
        end
    end

    // 输出控制
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            mac_dout <= 0;
        end else begin
            if(product_dout_vld) begin
                mac_dout <= product+addend_temp;
            end else begin
                mac_dout <= mac_dout;
            end
        end
    end

    // 输出有效位控制
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            mac_dout_vld <= 0;
        end else begin
            if(product_dout_vld) begin
                mac_dout_vld <= product_dout_vld;
            end else begin
                mac_dout_vld <= product_dout_vld;
            end
        end
    end

    // // Dump waves
    // initial begin
    //     $dumpfile("mac_unit.vcd");
    //     $dumpvars(1, mac_unit);
    // end

endmodule