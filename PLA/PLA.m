function count = PLA(w,combination,f2)
	  flag = 0;
    count = 0; 
    temp = w * combination';
    [m,n] = size(temp);
	   for i=1:n,
   	  	temp(:,i) = mySignFun(temp(:,i));
	   end
    for i=1:n,
   		if temp(:,i) ~= f2(i)
   		     w = w + f2(i) * combination(i,:);
		       count = count + 1;
   		     flag = 1;
  		     break;	
	    end
    end
    while( flag == 1)
           temp = w * combination';
    		[m,n] = size(temp);
   	    	 for i=1:n,
       			 temp(:,i) = mySignFun(temp(:,i));
    		end
   		 for i=1:n,
       		 if temp(:,i) ~= f2(i)
           		w = w + f2(i) * combination(i,:);
        	    count = count + 1;
				flag = 1;
        		break;
            else
               flag = 0;
            end  
    	end
    end