// 1. 往RAM按照顺序写数据
// 2. 更具有效信号获取需要合并的数据和读取数据
// 3. 合并数据
// 结构
//     |
//   layer ---
//     |      | branch
//   concat --
//     |

module concat_ram#(
    parameter N = 8,
    parameter INPUT_CHANNEL = 1,
    parameter INPUT_SIZE = 1,
    parameter RAM_ADDR_WIDTH = $clog2(INPUT_SIZE*INPUT_SIZE+1)
    )(
    input wire clk,
    input wire rst_n,

    // 主干输入，用于存入RAM
    input wire layer_vld,
    input wire [INPUT_CHANNEL*N-1:0] layer_din,

    // 分支输入，当输入有效时从RAM取数据进行合并
    input wire branch_vld,
    input wire [INPUT_CHANNEL*N-1:0] branch_din,

    // concat输出及有效位
    output reg concat_dout_vld,
    output reg [INPUT_CHANNEL*N*2-1:0] concat_dout
);
    reg [INPUT_CHANNEL*N-1:0] branch_din_temp;

    reg ram_wr_en;
    reg ram_rd_en;
    reg [RAM_ADDR_WIDTH-1:0] ram_wr_addr;
    reg [INPUT_CHANNEL*N-1:0] ram_wr_data;
    reg [RAM_ADDR_WIDTH-1:0] ram_rd_addr;
    wire [INPUT_CHANNEL*N-1:0] ram_rd_data;

    bram #(
        .RAM_WIDTH(INPUT_CHANNEL*N),
        .RAM_DEPTH(INPUT_SIZE*INPUT_SIZE),
        .ADDR_WIDTH(RAM_ADDR_WIDTH)
    ) dut_bram (
        .clk(clk),
        .wr_en(ram_wr_en),
        .rd_en(ram_rd_en),
        .wr_addr(ram_wr_addr),
        .wr_data(ram_wr_data),
        .rd_addr(ram_rd_addr),
        .rd_data(ram_rd_data)
    );

    /*************************写RAM操作*************************/

    // 写RAM使能控制
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            ram_wr_en <= 1'b0;
        end else begin
            if(layer_vld == 1'b1) begin
                ram_wr_en <= 1'b1;
            end else begin
                ram_wr_en <= 1'b0;
            end
        end
    end

    // 写RAM数据控制
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            ram_wr_data <= 0;
        end else begin
            if(layer_vld == 1'b1) begin
                ram_wr_data <= layer_din;
            end else begin
                ram_wr_data <= ram_wr_data;
            end
        end
    end

    // 写RAM地址控制
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            // 初始为FFFF，目的是第一次自加后可以从0开始存
            ram_wr_addr <= {RAM_ADDR_WIDTH{1'b1}};
        end else begin
            if(layer_vld == 1'b1) begin
                ram_wr_addr <= ram_wr_addr + 1'b1;
            end else if(ram_wr_addr >= (INPUT_SIZE*INPUT_SIZE-1)) begin
                ram_wr_addr <= {RAM_ADDR_WIDTH{1'b1}};
            end else begin
                ram_wr_addr <= ram_wr_addr;
            end
        end
    end

    /*************************读RAM操作*************************/

    // 读RAM使能控制
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            ram_rd_en <= 1'b0;
        end else begin
            if(branch_vld == 1'b1) begin
                ram_rd_en <= 1'b1;
            end else begin
                ram_rd_en <= 1'b0;
            end
        end
    end

    // 读RAM地址控制
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            // 初始为FFFF，目的是第一次自加后可以从0开始存
            ram_rd_addr <= {RAM_ADDR_WIDTH{1'b1}};
        end else begin
            if(branch_vld == 1'b1) begin
                ram_rd_addr <= ram_rd_addr + 1'b1;
            end else if(ram_rd_addr >= (INPUT_SIZE*INPUT_SIZE-1)) begin
                ram_rd_addr <= {RAM_ADDR_WIDTH{1'b1}};
            end else begin
                ram_rd_addr <= ram_rd_addr;
            end
        end
    end


    /*************************数据合并*************************/
    // 暂存branch分支的值，用于后续合并
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            branch_din_temp <= 0;
        end else begin
            if(branch_vld == 1'b1) begin
                branch_din_temp <= branch_din;
            end else begin
                branch_din_temp <= branch_din_temp;
            end
        end
    end

    // ram数据晚ram_rd_en一个周期，因此打一拍
    reg ram_rd_en_d0;
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            ram_rd_en_d0 <= 1'b0;
        end else begin
            ram_rd_en_d0 <= ram_rd_en;
        end
    end

    // concat
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            concat_dout <= 0;
        end else begin
            if(ram_rd_en_d0 == 1'b1) begin
                concat_dout <= {branch_din_temp, ram_rd_data};
            end else begin
                concat_dout <= concat_dout;
            end
        end
    end

    // 输出有效位
    always @(posedge clk) begin
        if(rst_n == 1'b0) begin
            concat_dout_vld <= 1'b0;
        end else begin
            if(ram_rd_en_d0 == 1'b1) begin
                concat_dout_vld <= 1'b1;
            end else begin
                concat_dout_vld <= 1'b0;
            end
        end
    end


    // always @(posedge clk) begin
    //     if(rst_n == 1'b0) begin
    //     end else begin
    //     end
    // end

    // Dump waves
    initial begin
        $dumpfile("concat_ram.vcd");
        $dumpvars(1, concat_ram);
    end

endmodule