var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {

									type: 'bar',

									data: {

											labels: ["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"],
											datasets:
											[
												{
													data: [{%for price in price%} '{{price}}', {% endfor %}],
													label:["價錢"],
													backgroundColor:getRandomColor(),
													borderColor: 'rgba(255, 99, 132, 0.2)',
												},

												]
									},
									options: {

											scales: {
													xAxes: [{
																			display: true,
																			scaleLabel: {
																					display: true,
																					labelString: '交易月份'
																			}
																	}],
																	yAxes: [{
																			display: true,
																			scaleLabel: {
																					display: true,
																					labelString: '價錢'
																			}
																	}]
											},
									},

							})

var ctx1 = document.getElementById('myChart1').getContext('2d');
var myChart1 = new Chart(ctx1, {

									type: 'bar',

									data: {

														labels: ["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"],
														datasets:
														[
															{
																data: [{%for quantity in quantity%} '{{quantity}}', {% endfor %}],
																label:["數量"],
																backgroundColor:getRandomColor(),
																borderColor: 'rgba(255, 99, 132, 0.2)',
															},

															]
												},
									options: {

														scales: {
																xAxes: [{
																						display: true,
																						scaleLabel: {
																								display: true,
																								labelString: '交易月份'
																						}
																				}],
																				yAxes: [{
																						display: true,
																						scaleLabel: {
																								display: true,
																								labelString: '數量'
																						}
																				}]
														},
												},

							})


var ctx2 = document.getElementById('myChart2').getContext('2d');
var myChart2 = new Chart(ctx2, {

																type: 'bar',

																data: {

																					labels: [{%for i in town%} '{{i}}', {% endfor %}],
																					datasets:
																					[
																						{
																							data: [{%for i in t_price%} '{{i}}', {% endfor %}],
																							label:["價錢"],
																							backgroundColor:getRandomColor(),
																							borderColor: 'rgba(255, 99, 132, 0.2)',
																						},

																						]
																			},
																options: {

																					scales: {
																							xAxes: [{
																													display: true,
																													scaleLabel: {
																															display: true,
																															labelString: '地區'
																													}
																											}],
																											yAxes: [{
																													display: true,
																													scaleLabel: {
																															display: true,
																															labelString: '數量'
																													}
																											}]
																					},
																			},

														})



