module padding#(
	parameter N = 8,
	parameter CHANNEL = 3,
	parameter SIZE = 32,
	parameter PADDING = 1,
	parameter CLK_INTERVAL = 13		// N+5 padding输出的时钟周期，完全一一对应
	)(
	input wire clk,
	input wire rst_n,
	input wire ce,
	input wire input_vld,
	input wire [CHANNEL*N-1:0] input_din,
	output wire [CHANNEL*N-1:0] padding_dout,
	output reg padding_dout_vld,
	output reg padding_dout_end
);

	reg [31:0] cnt, cnt_line, cnt_gap;
	reg read_queue;	// 从queue中读信号，真正发生给queue模块使用，数据返回在read_queue的下一个时钟
	reg read_queue_d0;
	wire [CHANNEL*N-1:0] queue_out;
	reg dout_vld;	// padding输出有效位，但是从queue中读出需要一个时钟周期，因此后续需要打一拍

	assign padding_dout = (read_queue_d0 == 1'b0)? {CHANNEL*N{1'b0}}:queue_out;

	queue_reg #(.width(CHANNEL*N), .depth(3*SIZE-2)) dut_queue_reg(
		.clk(clk),
		.rst(rst_n),
		.ce(ce),
		.input_vld(input_vld),
		.read_flag(read_queue),
		.din(input_din),
		.dout(queue_out)
	);

	// 从queue中读出需要一个时钟周期，因此需要打一拍
	always @(posedge clk) begin
		if(rst_n == 1'b0) begin
			padding_dout_vld <= 1'b0;
		end else begin
			padding_dout_vld <= dout_vld;
		end
	end

	// 从queue中读出需要一个时钟周期，因此需要打一拍
	always @(posedge clk) begin
		if(rst_n == 1'b0) begin
			read_queue_d0 <= 1'b0;
		end else begin
			read_queue_d0 <= read_queue;
		end
	end

	always @(posedge clk) begin
		if(rst_n == 1'b0 || ce == 1'b0) begin
			cnt <= 0;
			cnt_line <= 0;
			cnt_gap <= 0;
			read_queue <= 0;

			// padding_dout <= 0;
			dout_vld <= 0;
			padding_dout_end <= 1'b1;
		end else if(ce == 1'b1) begin
			if(cnt < SIZE*SIZE) begin
				if(input_vld == 1'b1) begin
					padding_dout_end <= 1'b0;
					// cnt cnt_line从1开始算，并且要判断为1的时候其实是判断上一时刻为1
					// 因此判断cnt_line == 1即判断每一行的开头的时候是判断cnt_line == SIZE+2*PADDING
					if(cnt < (SIZE+2*PADDING) || cnt >= (SIZE+2*PADDING)*(SIZE+2*PADDING-1) || cnt_line == (SIZE+2*PADDING) || cnt_line == (SIZE+2*PADDING-1)) begin
						dout_vld <= 1'b1;
						// padding_dout <= 0;
					end else begin
						dout_vld <= 1'b1;
						read_queue <= 1'b1;
						// padding_dout <= queue_out;
					end
		
					cnt <= cnt + 1;
					cnt_line <= cnt_line + 1;
					if(cnt_line >= (SIZE+2*PADDING)) begin
						cnt_line <= 1;
					end
				end else begin
					dout_vld <= 1'b0;
					read_queue <= 1'b0;
				end
			end else begin
				cnt_gap <= cnt_gap + 1;
				if(cnt_gap >= CLK_INTERVAL) begin
					cnt_gap <= 0;

					if(cnt < (SIZE+2*PADDING) || cnt >= (SIZE+2*PADDING)*(SIZE+2*PADDING-1) || cnt_line == (SIZE+2*PADDING) || cnt_line == (SIZE+2*PADDING-1)) begin
						dout_vld <= 1'b1;
						// padding_dout <= 0;
					end else begin
						dout_vld <= 1'b1;
						read_queue <= 1'b1;
						// padding_dout <= queue_out;
					end
		
					cnt <= cnt + 1;
					cnt_line <= cnt_line + 1;
					if(cnt_line >= (SIZE+2*PADDING)) begin
						cnt_line <= 1;
					end
				end else begin
					dout_vld <= 1'b0;
					read_queue <= 1'b0;
				end
			end

			if(cnt >= (SIZE+2*PADDING)*(SIZE+2*PADDING)) begin
				padding_dout_end <= 1'b1;
				cnt <= 0;
				cnt_line <= 0;
				cnt_gap <= 0;
			end
		end
	end

	// Dump waves
	initial begin
		$dumpfile("padding.vcd");
		$dumpvars(1, padding);
	end


endmodule