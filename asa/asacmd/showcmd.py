from terminaltables import AsciiTable
from common import Utility
import time


class ShowCmd:
    def __init__(self, connect, config, ip_address):
        self.ip_address = ip_address
        self.connect = connect
        self.mode_multiple = None
        self.context_list = None
        self.command_list = config.get_command_list
        self.get_show_output_path = config.get_show_output_path
        if(self.is_mode_multiple):
            self.mode_multiple = True
            self.context_list = self.get_all_context()


    @property
    def is_mode_multiple(self):
        output = self.connect.send_command("show mode")
        if('multiple' in output):
            return True
        else:
            return False

    def get_all_context(self):
        '''
        {'adminctx': 'ctxadm',
        'allctx': ['ctxadm', 'ctxgendr-ct', 'ctxgendr-rs', 'ctxgennp-ct']}
        :return:
        '''
        self.connect.send_command("changeto context system")
        output = self.connect.send_command("show run context", use_textfsm=True)
        output[1]['adminctx'] = output[0]['adminctx']
        return output[1]


    def show_traffic(self):
        output = self.connect.send_command("show traffic")
        lines = [item.strip() for item in output.splitlines() if item.strip() != '']
        remove_line = '----------------------------------------'
        remove_aggregated = 'Aggregated Traffic on Physical Interface'
        if remove_line in lines: lines.remove(remove_line)
        if remove_aggregated in lines: lines.remove(remove_aggregated)
        if remove_line in lines: lines.remove(remove_line)
        main_list = []
        header = ['Interface', 'received',
                  '1mir pks/s', '1mir bs/s',
                  '1mor pks/s', '1mor bs/s',
                  '1mdr pks/s',
                  '5mir pks/s', '5mir bs/s',
                  '5mor pks/s', '5mor bs/s',
                  '5mdr pks/s']
        main_list.append(header)
        sublist = []
        i = 1
        k = 1
        for line in lines:
            if ('received' in line):
                sublist.append(line.strip().split(' ')[2])
                print(line)
            if ('1 minute input rate' in line):
                print(line.strip().split(' '))
                sublist.append(line.strip().split(' ')[4])
                sublist.append(line.strip().split(' ')[7])
            if ('1 minute output rate' in line):
                print(line.strip().split(' '))
                sublist.append(line.strip().split(' ')[4])
                sublist.append(line.strip().split(' ')[7])
            if ('1 minute drop rate' in line):
                print(line.strip().split(' '))
                sublist.append(line.strip().split(' ')[4])
            if ('5 minute input rate' in line):
                print(line.strip().split(' '))
                sublist.append(line.strip().split(' ')[4])
                sublist.append(line.strip().split(' ')[7])
            if ('5 minute output rate' in line):
                print(line.strip().split(' '))
                sublist.append(line.strip().split(' ')[4])
                sublist.append(line.strip().split(' ')[7])
            if ('5 minute drop rate' in line):
                print(line.strip().split(' '))
                sublist.append(line.strip().split(' ')[4])
            if (i == 1):
                sublist.append(line.strip(':'))
                i = i + 1
                k = k + 13
                continue
            if (i == k):
                k = k + 13
                main_list.append(sublist)
                sublist = []
                sublist.append(line.strip(':'))
            i = i + 1
        main_list.append(sublist)
        print(main_list)
        table = AsciiTable(main_list)
        print(table.table)

    def run_command_list(self):
        if(self.mode_multiple):
            outputs = []
            allctx = self.get_all_context()
            for context in allctx['allctx']:
                self.connect.send_command('changeto context {}'.format(context))
                outputs.append('\n==============================================================================\n')
                outputs.append('changeto context {}'.format(context))
                outputs.append('\n==============================================================================\n')
                for command in self.command_list:
                    outputs.append('*********************************')
                    outputs.append(command)
                    outputs.append('*********************************\n')
                    outputs.append(self.connect.send_command(command))
            self.connect.send_command('changeto context system')
            outputs.append('\n==============================================================================\n')
            outputs.append('changeto context system')
            outputs.append('\n==============================================================================\n')
            for command in self.command_list:
                outputs.append('*********************************')
                outputs.append(command)
                outputs.append('*********************************\n')
                outputs.append(self.connect.send_command(command))
                outputs.append('\n==============================================================================\n')
            self.output_to_file(outputs)

        else:
            outputs = []
            for command in self.command_list:
                outputs.append('*********************************')
                outputs.append('command')
                outputs.append('*********************************')
                outputs.append(self.connect.send_command(command))
            self.output_to_file(outputs)

    def output_to_file(self, outputs):
        time_string = time.strftime("%Y_%m_%d_%H_%M_%S")
        file_name = '{}/{}_{}.txt'.format(self.get_show_output_path, self.ip_address, time_string)
        with open(file_name, "w") as f:
            for output in outputs:
                f.write(str(output))

    def show_cpu(self):
        pass

    def show_memory(self):
        pass

    def show_performance(self):
        pass

    def show_blocks(self):
        pass

    def show_conn_count(self):
        pass

    def show_interface(self):
        pass

    def show_process(self):
        pass
